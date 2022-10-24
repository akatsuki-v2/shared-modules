from setuptools import setup

requirements = []
with open("requirements.txt", "r") as f:
    for raw_req in f.read().splitlines():
        # TODO: dear god this is not it
        if raw_req.startswith("git+"):
            req_name = raw_req.rsplit("/", 1)[1]
            requirements.append(f"{req_name} @ {raw_req}")
        else:
            requirements.append(raw_req)

setup(
    install_requires=requirements,
)
