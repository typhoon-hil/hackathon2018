from hackathon.energy.energy_math import gen_profile
from hackathon.utils.utils import *
import json

__author__ = "Dusan Majstorovic"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"


def generate_profiles():
    # Training profiles
    #LOAD_SCALES = [1.0, 1.1, 0.8, 1.2, 0.9]
    #SOLAR_SCALES = [1.3, 0.4, 0.8, 0.9, 1.1]
    #BLACKOUTS = [[[11, 11.75]],
    #             [],
    #             [[2.5,3]],
    #             [[20,21]],
    #             [],
    #             ]

    # Competition profiles
    LOAD_SCALES = [1.0, 0.8, 0.9, 1.1, 1.2]
    SOLAR_SCALES = [1.0, 1.5, 1.2, 0.9, 0.5]
    BLACKOUTS = [[[22.75,23.25]],
                 [],
                 [[13.0,14.0]],
                 [[2.5,3.25]],
                 [[18.5,19.25]],
                 ]


    PROFILES = []

    # used to smoothen out the load PROFILES on day transitions
    LOAD_SCALING_PREV = 1.0

    for i in CFG.days:
        n = i-1
        to_write, profile = gen_profile(CFG.sampleRate,
                                        load_scaling=LOAD_SCALES[n],
                                        load_scaling_prev=LOAD_SCALING_PREV,
                                        solar_scaling=SOLAR_SCALES[n],
                                        blackouts=BLACKOUTS[n])
        PROFILES += profile
        LOAD_SCALING_PREV = LOAD_SCALES[n]

    with open('./data/profiles_cmp.json', 'w') as f:
        f.write(json.dumps(PROFILES))

    print('Profile is generated in {}'.format('./data/profiles_cmp.json'))


if __name__ == '__main__':
    generate_profiles()