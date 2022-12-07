from . import sublist3r
import time
import concurrent.futures
import subprocess
import json
import re

subdomains=[]
def domain_search(domain_name,filename=None):
    #subdomains = sublist3r.main('bitmesra.ac.in', 10, savefile=None, ports= None, silent=True, verbose= False, enable_bruteforce= False, engines='dnsdumpster,bing,ssl')
    subdomains = sublist3r.main(domain_name, 10, savefile=filename, ports= None, silent=True, verbose= False, enable_bruteforce= False, engines='dnsdumpster,bing,ssl')
    return subdomains


def subdomain_extractor(domain,filename=None):
    subdomains=[]
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        future = executor.submit(domain_search, domain,filename)
        return_value = future.result()
        subdomains = return_value
    print("Printing Subdomains".center(80,'-'))
    filtered_subdomains=[]
    for i in subdomains:
        if(i.startswith("www")):
            continue
        filtered_subdomains.append(i)
    print(filtered_subdomains)
    with open(filename,"w+") as f:
        f.write("\n".join(filtered_subdomains))
    return filtered_subdomains


def subdomain_detail_extractor(filename):
    # print("Printing Subdomains detailed output".center(80,'-'))
    output = subprocess.check_output(f'httpx -l {filename} -cname -td -json -silent',shell=False).splitlines()
    subdomain_detail=[]
    for i in output:
        data = json.loads(i.decode())
        temp_dict={
            "subdomain_name":data.get("input",""),
            "cname":data.get("cname",""),
            "web_server":data.get("webserver",""),
            "ip":data.get("host",""),
            "page_title":data.get("title",""),
            "status_code":data.get("status_code",""),
            "content_length":data.get("content_length",""),
            "content_type":data.get("content_type",""),
            "tech_stack_detect":data.get("tech",""),
            "response_time":data.get("time",""),
        }
        subdomain_detail.append(temp_dict)
    # print(subdomain_detail)
    return subdomain_detail
    
    

def subdomain_port_extractor(filename):
    # print("Printing Subdomain ports".center(80,'-'))
    output = subprocess.check_output(f'naabu -l {filename} -json -silent',shell=False).splitlines()
    ports_list=dict()
    for i in output:
        data = json.loads(i.decode())
        if data["host"] in ports_list:
            ports_list[data["host"]].append(data.get("port",""))
        else:
            ports_list[data["host"]]=[data.get("port","")]
    # print(ports_list)
    return ports_list
    


def subdomain_image_extractor(filename,directory_of_screenshots,subdomains):
    # print("Printing Subdomain screenthosts output".center(80,'-'))
    _ = subprocess.check_output(f'gowitness file -f {filename} -P {directory_of_screenshots} --no-http --disable-logging',shell=False)
    screenshot_path_list=[]
    for i in subdomains:
        temp_dict={
            "subdomain_name":i,
            "screenshot_path":"https://"+i+".png"
            }
        screenshot_path_list.append(temp_dict)
    # print(screenshot_path_list)
    return screenshot_path_list
    
    

def domain_enumerator(domain):
    filename="temp_test.txt"
    result=[]
    # domain="hakhub.net"
    directory_of_screenshots="images"
    subdomains = subdomain_extractor(domain,filename)
    if len(subdomains)==0:
        return result

    #subdomain detail extrator
    # subdomain_detail_extractor(filename)

    #subdomain active port extractor
    # subdomain_port_extractor(filename)

    #subdomain image extractor
    # subdomain_image_extractor(filename,directory_of_screenshots,subdomains)
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
    
        detail_extractor=executor.submit(subdomain_detail_extractor,filename)
        port_extractor=executor.submit(subdomain_port_extractor,filename)
        image_extractor=executor.submit(subdomain_image_extractor,filename,directory_of_screenshots,subdomains)

        result.append({"ports":port_extractor.result()})
        result.append({"details":detail_extractor.result()})
        result.append({"images":image_extractor.result()})

    return result

# main program
if __name__=="__main__":
    start_time=time.perf_counter()
    domain_enumerator("hakhub.net")
    end_time=time.perf_counter()
    print(f"Program finished in {round(end_time-start_time,4)} seconds")
