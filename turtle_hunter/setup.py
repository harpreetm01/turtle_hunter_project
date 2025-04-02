from setuptools import find_packages, setup

package_name = "turtle_hunter"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="harpreet",
    maintainer_email="harpreet@todo.todo",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "turtle_spawner = turtle_hunter.turtle_spawner:main",
            "turtle_controller = turtle_hunter.turtle_controller:main",
        ],
    },
)
