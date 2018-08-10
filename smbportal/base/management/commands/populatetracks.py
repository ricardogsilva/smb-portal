#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import datetime as dt
import pathlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from lxml import etree
import pytz

from keycloakauth.keycloakadmin import get_manager
from keycloakauth.utils import create_user
from vehicles.models import Bike
import profiles.models as pm
from tracks import models


class Command(BaseCommand):
    help = (
        "Add test data for tracks. This command adds users, bikes, tracks and "
        "collected points to the database. The users are created also on "
        "keycloak. Usernames of the new users: `track_tester1`, "
        "`track_tester2` and `track_tester3`"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keycloak_manager = get_manager(
            settings.KEYCLOAK["base_url"],
            settings.KEYCLOAK["realm"],
            settings.KEYCLOAK["client_id"],
            settings.KEYCLOAK["admin_username"],
            settings.KEYCLOAK["admin_password"],
        )

    def add_arguments(self, parser):
        default_gpx_path = pathlib.Path(
            settings.BASE_DIR).parent / "tests" / "data" / "tracks.gpx"
        parser.add_argument(
            "--gpx-file-path",
            help="Path to a gpx file with tracks to add. Defaults to "
                 "%(default)r",
            default=str(default_gpx_path)
        )

    def handle(self, *args, **options):
        gpx_path = pathlib.Path(
            options["gpx_file_path"],
        )
        owners = {
            "track_tester1": {
                "age": pm.EndUserProfile.AGE_BETWEEN_NINETEEN_AND_THIRTY,
                "occupation": pm.EndUserProfile.OCCUPATION_ARCHITECT,
            },
            "track_tester2": {
                "age": pm.EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE,
                "occupation": pm.EndUserProfile.OCCUPATION_FREELANCER,
            },
            "track_tester3": {
                "age": pm.EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE,
                "occupation": pm.EndUserProfile.OCCUPATION_UNEMPLOYED,
            },
        }
        self.stdout.write("Creating test users and bikes...")
        try:
            users = create_test_users(owners, self.keycloak_manager)
        except RuntimeError as exc:
            self.stderr.write("{} - Aborting".format(str(exc)))
        else:
            self.stdout.write("Parsing gpx file...")
            all_tracks = get_tracks_from_gpx(gpx_path)
            self.stdout.write("Creating tracks and points...")
            save_tracks(all_tracks, users)
        self.stdout.write("Done!")


def create_test_users(users_info, keycloak_manager):
    if users_exist(users_info.keys()):
        raise RuntimeError("Users already exist")
    users = []
    for index, user_info in enumerate(users_info.items()):
        username, profile_kwargs = user_info
        user = create_user(
            username,
            email="{}@fake.com".format(username),
            password="123456",
            group_path="/end_users",
            keycloak_manager=keycloak_manager,
            profile_model=pm.EndUserProfile,
            profile_kwargs=profile_kwargs
        )
        for bike_index in range(2):
            nickname = "bike_{}_{}".format(index, bike_index)
            Bike.objects.create(nickname=nickname, owner=user)
        users.append(user)
    return users


def users_exist(usernames: list) -> bool:
    return pm.SmbUser.objects.filter(
        username__in=usernames).count() != 0


@transaction.atomic
def save_tracks(imported_tracks, users):
    owner_info = _unfold_users(users)
    for track_index, imported_track in enumerate(imported_tracks):
        owner_index = _map_track_to_user(
            len(owner_info), len(imported_tracks), track_index)
        username, bike_nickname = owner_info[owner_index]
        user = get_user_model().objects.get(username=username)
        bike = Bike.objects.get(owner=user, nickname=bike_nickname)
        save_track(user, bike, imported_track)


def save_track(user, bike, track_points):
    track = models.Track.objects.create(owner=user)
    for pt_index, point in enumerate(track_points):
        if pt_index < len(track_points) * 0.9:
            vehicle_id = bike.id
            vehicle_type = models.BIKE
        else:
            vehicle_id = None
            vehicle_type = models.BUS
        models.CollectedPoint.objects.create(
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            track=track,
            the_geom=Point(point["lon"], point["lat"]),
            timestamp=point.get("timestamp"),
        )
    return track


def get_tracks_from_gpx(gpx_path: pathlib.Path):
    """Generate collected points from a gpx file

    We transform each of the GPX's track segment into a track

    """

    gpx = etree.fromstring(
        gpx_path.read_bytes(),
        parser=etree.XMLParser(resolve_entities=False)
    )
    nsmap = {
        "gpx": gpx.nsmap[None]
    }
    track_segments = gpx.xpath("gpx:trk/gpx:trkseg", namespaces=nsmap)
    tracks = []
    for segment_element in track_segments:
        segment = []
        for point in segment_element.xpath("gpx:trkpt", namespaces=nsmap):
            collected_point = {
                "lat": float(point.get("lat")),
                "lon": float(point.get("lon")),
            }
            try:
                point_date = _get_time(
                    point.xpath("gpx:time/text()", namespaces=nsmap)[0]
                )
            except IndexError:
                pass
            else:
                collected_point["timestamp"] = point_date
            segment.append(collected_point)
        tracks.append(segment)
    return tracks


def _unfold_users(users):
    owner_info = []
    for user in users:
        for bike in user.bikes.all():
            owner_info.append((user, bike))
    return owner_info


def _get_time(raw_time: str):
    return pytz.utc.localize(
        dt.datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
    )


def _map_track_to_user(num_users, num_tracks, current_track):
    return int(current_track / num_tracks * num_users)
