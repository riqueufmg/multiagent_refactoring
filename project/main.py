from agents.detecting_agent import DetectingAgent

def main():
    project_path = "data/repositories/jsoup"
    processed_path = "data/processed/metrics/jsoup"
    classes_path = "data/repositories/jsoup/target/classes"
    
    detector = DetectingAgent(project_path, processed_path, classes_path)
    detector.run()
    
if __name__ == "__main__":
    main()