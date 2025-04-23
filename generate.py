from generator.parser import load_config
from generator.code_writer import write_endpoints
import os

if __name__ == "__main__":
    template_name="example"
    directory=f"generated_apis/{template_name}"
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    config = load_config(f"templates/{template_name}.yaml")
    write_endpoints(config,output_dir=directory)
    print("✅ API code generated in ./generated_api/")
