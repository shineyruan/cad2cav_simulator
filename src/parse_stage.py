import pxr.Usd
import pxr.UsdGeom
import numpy as np


class StageParser:

  def __init__(self, stage: pxr.Usd.Stage) -> None:
    self.stage = stage

  def traverse_and_print(self) -> None:
    for component in self.stage.Traverse():
      if component.GetPath().HasPrefix("/World/Floor_2/Geometry/FamilyData"):
        continue
      if component.GetPath().HasPrefix("/World/Floor_2/Geometry/Generic"):
        continue
      if component.GetPath().HasPrefix(
          "/World/Floor_2/Geometry/Generic_Models"):
        continue
      if component.HasProperty("familyInstanceInfo"):
        attribute = str(component.GetAttribute("familyInstanceInfo").Get())
        print(attribute.split(',')[0])
        mat_transform = np.array(
            component.GetAttribute("xformOp:transform").Get().GetTranspose())
        print(mat_transform)
        print("")

  def traverse(self) -> dict:
    waypoints = {}
    for component in self.stage.Traverse():
      if component.GetPath().HasPrefix("/World/Floor_2/Geometry/FamilyData"):
        continue
      if component.GetPath().HasPrefix("/World/Floor_2/Geometry/Generic"):
        continue
      if component.GetPath().HasPrefix(
          "/World/Floor_2/Geometry/Generic_Models"):
        continue

      if component.HasProperty("familyInstanceInfo"):
        attribute = str(component.GetAttribute("familyInstanceInfo").Get())
        mat_transform = np.array(
            component.GetAttribute("xformOp:transform").Get().GetTranspose())
        if attribute.split(',')[0] not in waypoints.keys():
          waypoints[attribute.split(',')[0]] = [mat_transform]
        else:
          waypoints[attribute.split(',')[0]].append(mat_transform)

    for name in waypoints.keys():
      waypoints[name] = np.stack(waypoints[name])

    return waypoints
