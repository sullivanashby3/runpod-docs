import argparse
def compare(gpu_hourly,gpu_seconds_per_output,api_per_second,seconds):
 gpu=gpu_hourly/3600*seconds/gpu_seconds_per_output
 api=api_per_second*seconds
 return {'gpu_estimate':round(gpu,6),'api_estimate':round(api,6),'assumptions':{'gpu_hourly':gpu_hourly,'throughput':gpu_seconds_per_output}}
def main():
 p=argparse.ArgumentParser();p.add_argument('--gpu-hourly',type=float,required=True);p.add_argument('--throughput',type=float,required=True);p.add_argument('--api-rate',type=float,required=True);p.add_argument('--seconds',type=float,default=60);a=p.parse_args();print(compare(a.gpu_hourly,a.throughput,a.api_rate,a.seconds))
if __name__=='__main__':main()
