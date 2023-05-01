from src.linkedin.api import API
from src.linkedin.user import User
from rich import print
import os

os.environ[
    "LINKEDIN_TOKEN"
] = "AQUsFm3ywriXg7JvgFCXW3uSsnI5lmvhq1cmzbrN0FRQK1FRRbdkxIo7w9SpQ09fb4hxWoO22mJb8_6Llox5PuBxpE8GpweThQy0xqAwcD2Ni8LDFo4q0i_0RG3THsBVDn_WgXRryzvIW0vlCuM2aUQmsvPzQR2fHjqSYb-k5n_nOgA6Ak7SRQ1lcF92yoN-R22M_ovaVXxfhK0MpHIKEe89BJRaSIdA_TPIsBAjO3gQiY2KLz2cZyDV1JXSW5ukeEK-nD2eROv10rWFL-3J4gWiIBw886J-PdArTZquhEyEGUV056ggAtLnevO8gjveNasJ912Rw8Qmc0ZRvoTK5c0ros56ZQ"

api = API.from_env()

user = User()
res = user.create_post(
    "test from my custom python APIs with two images",
    images=[
        ("/home/zuppif/Documents/LinkedInGPT/grogu.jpg", "grogu"),
        ("/home/zuppif/Documents/LinkedInGPT/grogu_2.png", "grogu2"),
    ],
)
