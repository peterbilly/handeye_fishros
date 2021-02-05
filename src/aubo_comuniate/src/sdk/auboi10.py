from robotcontrol import * 
import os.path,sys,json

def save_file(path,data):
    if str(path).startswith("~"):
        path = path.replace("~",str(os.getenv("HOME")))
    with open(path,'a') as wf:
        wf.write(str(data))
        wf.close()
        
def main():
    # logger_init()
    Auboi5Robot.initialize()

    robot = Auboi5Robot()
    handle = robot.create_context()
    try:
        ip = '10.55.17.126'
        port = 8899
        result = robot.connect(ip, port)

        tool =  { "pos": (0.019554, 0.008029, 0.259355), "ori": (1.0, 0.0, 0.0, 0.0) }

        if result != RobotErrorType.RobotError_SUCC:
            logger.info("connect server{0}:{1} failed.".format(ip, port))
        else:
            data = ""
            while True:
                # sys.stdout.write("input command:\n")
                # sys.stdout.flush()
                # command = sys.stdin.readline().strip()
                command = input("")
                if command == "r":
                    r=robot.get_current_waypoint()
                    # r = robot.base_to_base_additional_tool(r['pos'],r['ori'],tool)
                    data =  json.dumps(r) + "\n"
                    sys.stdout.write(data)
                    save_file("./data.txt",data)
                    # break
                sys.stdout.flush()    
            robot.disconnect()
    except Exception as e:
        pass
    finally:
        if robot.connected:
            robot.disconnect()
        Auboi5Robot.uninitialize()

main()