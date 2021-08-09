from simulator import Simulator
from parse_stage import StageParser


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("USD Loader")
    parser.add_argument("--usd_path", type=str, help="Path to usd file", required=True)
    parser.add_argument("--headless", default=False, action="store_true", help="Run stage headless")

    args, unknown = parser.parse_known_args()
    simulator = Simulator(args.headless)
    if simulator.load_stage(args.usd_path):
        print("Loading stage...")
        while simulator.kit.is_loading():
            simulator.kit.update(1.0 / 60.0)
        print("Loading complete!")

        # parse and analyze prior information from stage
        stage_parser = StageParser(simulator.get_stage())
        waypoints = stage_parser.traverse()

        # start simulation
        simulator.start()
        while simulator.kit.app.is_running():
            simulator.kit.update()
        simulator.stop()
