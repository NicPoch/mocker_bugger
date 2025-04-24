import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("generator/templates"))

def sanitize_path(path):
    return path.strip("/").replace("/", "_").replace("-", "_")

def render_enpoint(config, output_dir):
    print("Rendering domain endpoints")
    os.makedirs(f"{output_dir}/endpoints", exist_ok=True)
    
    imports = []
    includes = []
    for domain in config["domains"]:
        print(f"Rendering domain: {domain['name']}")
        endpoints = []
        extra_imports = {
            "delay":False,
            "errors":False
        }
        filename = sanitize_path(domain["name"]) or "root"
        prefix = f"/{domain['name']}"
        for ep in domain["endpoints"]:
            print(f"\t{ep['path']}")
            endpoint_template = env.get_template("endpoint_template.j2")
            function_name = f"{ep['method'].lower()}_{filename}" + ("" if ep["path"]=="/" else ep["path"][1:])
            extra_imports["delay"]= extra_imports["delay"] or "delay" in ep
            extra_imports["errors"]=extra_imports["errors"] or ep["response"]["status_code"]<200 or ep["response"]["status_code"]>=300
            endpoint_render = endpoint_template.render(
                method=ep["method"],
                function_name=function_name,
                delay=ep.get("delay"),
                status_code=ep["response"]["status_code"],
                response_body=ep["response"]["body"],
                path=prefix+ep["path"]
            )
            endpoints.append(endpoint_render)

        domain_template = env.get_template("domain_template.j2")
        rendered = domain_template.render(
            errors = extra_imports["errors"],
            delay=extra_imports["delay"],
            endpoints=endpoints
        )

        filepath = f"{output_dir}/endpoints/{filename}.py"
        with open(filepath, "w") as f:
            f.write(rendered)
        imports.append(f"from endpoints import {filename}")
        includes.append(f"app.include_router({filename}.router)")
    return imports, includes

def render_requirements(requirements_config,output_dir):
    requirements_template = env.get_template("requirements_template.j2")
    requirements_rendered = requirements_template.render(
            requirements=requirements_config
        )
    filepath = f"{output_dir}/requirements.txt"
    with open(filepath, "w") as f:
        f.write(requirements_rendered)

def render_cors(app_config):
    cors_template = env.get_template("cors_template.j2")
    cors_rendered = cors_template.render(
            origins = app_config["cors"].get("origins",["*"]),
            credentials = app_config["cors"].get("credentials",True) ,
            methods = app_config["cors"].get("methods",["*"]) ,
            headers = app_config["cors"].get("headers",["*"]) 
        )
    return cors_rendered

def render_main(config, output_dir,imports,includes):
    app_config = config["app"]
    main_template = env.get_template("main_template.j2")
    main_rendered = main_template.render(
            imports=imports,
            routes=includes,
            cors = render_cors(app_config) if "cors" in app_config else None
        )
    with open(f"{output_dir}/main.py", "w") as f:
        f.write(main_rendered)

def write_application(config, output_dir="generated_api"):
    imports, includes = render_enpoint(config, output_dir)
    render_main(config, output_dir,imports,includes)
    render_requirements(config["requirements"],output_dir)
    
