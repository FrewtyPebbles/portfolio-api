import json
import os
import pathlib as pl


def docs_grabber(program_name:str):
    ret_val = {}
    cache_file = pl.Path("static", "projects", program_name, "cache", "docs.json")
    if cache_file.exists():
        pages = {}
        docs_path = pl.Path("static", "projects", program_name, "docs")
        if docs_path.exists():
            for raw_file in os.listdir(docs_path):
                file = pl.Path(raw_file)
                file_and_ext = file.name.split(".")
                f_obj = open(pl.Path("static", "projects", program_name, "docs", file.name).absolute())
                pages[file_and_ext[1]] = f_obj.read()
                f_obj.close()
            
        wf_obj = open(cache_file, "w")
        json.dump({"pgs":pages}, wf_obj)
        wf_obj.close()
        ret_val = {"pgs":pages}
    
    else:
        cache_json = open(cache_file)
        ret_val = json.load(cache_json)
    
    return ret_val

def project_grabber(program_name:str, path:str):
    ret_val = {}
    cache_file = pl.Path("static","projects", program_name, "cache", "project.json")
    
    if cache_file.exists():
        f_path = pl.Path("static", "projects", program_name, path)
        client_path = pl.Path("projects", program_name, path)
        stack = [{},{}]

        if f_path.exists():
            def into_dir():
                nonlocal client_path
                nonlocal stack
                nonlocal f_path
                
                dir = f_path
                for raw_file in os.listdir(dir):
                    file = pl.Path(f_path, raw_file)
                    
                    if file.is_file():
                        if (file.name.split(".")[1] in {"jpg","jpeg","png"}) \
                            if "." in file.name else False:
                            stack[len(stack)-1][str(pl.Path(client_path, file.name))] = f"http://127.0.0.1:5000/{str(pl.Path(f_path, file.name))}"
                        else:
                            try:
                                f_obj = open(pl.Path(f_path, file.name))
                                stack[len(stack)-1][str(pl.Path(client_path, file.name))] = f_obj.read()
                                f_obj.close()
                            except:
                                stack[len(stack)-1][str(pl.Path(client_path, file.name))] = "Cannot render binaries with UTF-8 characters."
                    elif file.is_dir():
                        client_path = pl.Path(client_path, file.name)
                        f_path = pl.Path(f_path, file.name)
                        stack.append({})
                        into_dir()
                        client_path = client_path.parent
                        f_path = f_path.parent
                
                laststack = stack[len(stack)-1]
                stack[len(stack)-2][str(client_path)] = laststack
                stack.pop()
                return
            into_dir()
        wf_obj = open(cache_file, "w")
        json.dump({"root":stack[0]}, wf_obj)
        wf_obj.close()

        ret_val = {"root":stack[0]}
    
    else:
        cache_json = open(cache_file)
        ret_val = json.load(cache_json)
    
    return ret_val