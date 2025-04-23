import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("generator/templates"))

def sanitize_path(path):
    return path.strip("/").replace("/", "_").replace("-", "_")

def write_endpoints(config, output_dir="generated_api"):
    os.makedirs(f"{output_dir}/endpoints", exist_ok=True)
    
    imports = []
    includes = []

    for ep in config["endpoints"]:
        template = env.get_template("endpoint_template.j2")
        filename = sanitize_path(ep["path"]) or "root"
        function_name = f"{ep['method'].lower()}_{filename}"

        rendered = template.render(
            path=ep["path"],
            method=ep["method"],
            response_body=ep["response"]["body"],
            status_code=ep["response"]["status_code"],
            delay=ep.get("delay",None),
            function_name=function_name
        )

        filepath = f"{output_dir}/endpoints/{filename}.py"
        with open(filepath, "w") as f:
            f.write(rendered)

        imports.append(f"from endpoints import {filename}")
        includes.append(f"app.include_router({filename}.router)")

    main_template = env.get_template("main_template.j2")
    main_rendered = main_template.render(
            imports=imports,
            routes=includes
        )
    with open(f"{output_dir}/main.py", "w") as f:
        f.write(main_rendered)
