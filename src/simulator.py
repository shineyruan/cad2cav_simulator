import os
from omni.isaac.python_app import OmniKitHelper
import carb
import omni
import pxr.Usd

# This sample loads a usd stage and creates a robot engine bridge application and starts simulation
# Disposes average fps of the simulation for given time
# Useful for testing an Isaac SDK sample scene using python
CONFIG = {
    "experience": f'{os.environ["EXP_PATH"]}/omni.isaac.sim.python.kit',
    "width": 1280,
    "height": 720,
    "sync_loads": True,
    "headless": False,
    "renderer": "RayTracedLighting",
}


class Simulator:

  def __init__(self, run_headless: bool) -> None:
    CONFIG['headless'] = run_headless
    self.kit = OmniKitHelper(config=CONFIG)
    self.usd_path = ""

    # enable ROS bridge extension
    ext_manager = omni.kit.app.get_app().get_extension_manager()
    ext_manager.set_extension_enabled_immediate("omni.isaac.ros_bridge", True)

  def start(self) -> None:
    self.kit.play()

  def stop(self):
    self.kit.stop()
    omni.kit.commands.execute("RobotEngineBridgeDestroyApplication")
    self.kit.shutdown()

  def load_stage(self, usd_path: str) -> bool:
    from omni.isaac.utils.scripts.nucleus_utils import find_nucleus_server

    result, nucleus_server = find_nucleus_server()
    if result is False:
      carb.log_error("Could not find nucleus server with /Isaac folder")
      return False

    self.usd_path = os.path.join(nucleus_server, usd_path)
    omni.usd.get_context().open_stage(self.usd_path, None)

    # Wait two frames so that stage starts loading
    self.kit.app.update()
    self.kit.app.update()
    return True

  def get_stage(self) -> pxr.Usd.Stage:
    return omni.usd.get_context().get_stage()
