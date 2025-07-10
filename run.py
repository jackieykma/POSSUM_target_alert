from io import StringIO
import os
import sys
import argparse
import numpy as np
import POSSUM.survey_coverage.covered_by_POSSUM as cbp



docstring = '''
Will need to write brief documentation here
'''





def main(args):
   ## Save output channel name
   out_channel_list = args.channel.split(',')
   del args.channel
   ## Move to correct working directory
   os.chdir('POSSUM/survey_coverage')
   if args.file_path[0] != '/':
      ## If relative path, correct path after chdir
      args.file_path = '../../'+args.file_path
   ## Save the path to output file, and remove from args
   output_path = args.output
   del args.output
   if output_path[0] != '/':
      output_path = '../../'+output_path
   
   
   ## Redirect print output to string
   old_stdout = sys.stdout
   sys.stdout = mystdout = StringIO()
   ## First run for Band 1
   args.band = '1'
   cbp.main(args)
   band1_output = mystdout.getvalue().split('\n')
   ## Then run for Band 2
   sys.stdout = mystdout = StringIO()
   args.band = '2'
   cbp.main(args)
   band2_output = mystdout.getvalue().split('\n')
   ## Revert back the print output method
   sys.stdout = old_stdout
   
   
   ## Search through the output for string "Status: OBSERVED"
   band1_output = np.array(band1_output)
   band2_output = np.array(band2_output)
   band1_observed_idx = np.array(range(len(band1_output)))[band1_output == 'Status: OBSERVED']
   band2_observed_idx = np.array(range(len(band2_output)))[band2_output == 'Status: OBSERVED']
   ## For observed sources, get source name, SBID info, etc
   band = '1';  band1_list = [] ## Array to store results for Band 1
   if len(band1_observed_idx) > 0:
      for src_idx in band1_observed_idx:
         src_name = band1_output[src_idx-1]
         src_name = src_name.split('location ')[-1][:-3]
         i = 1 ## Read line-by-line for observed tiles
         while band1_output[src_idx+i][0:7] != 'Belongs':
            sbid_info = band1_output[src_idx+i].split(', ')
            i += 1
            ## Unpack everything
            print(sbid_info)
            tile = sbid_info[0][7:]
            sbid = sbid_info[1][7:].split('.')[0] ## Remove trailing ".0"
            beamno = sbid_info[2][10:]
            beamsep = sbid_info[3][12:]
            ## Save all information
            band1_list.append([band, src_name, tile, sbid, beamno, beamsep])
   ## Repeat the above for Band 2
   band = '2';  band2_list = [] ## Array to store results for Band 2
   if len(band2_observed_idx) > 0:
      for src_idx in band2_observed_idx:
         src_name = band2_output[src_idx-1]
         src_name = src_name.split('location ')[-1][:-3]
         i = 1 ## Read line-by-line for observed tiles
         while band2_output[src_idx+i][0:7] != 'Belongs':
            sbid_info = band2_output[src_idx+i].split(', ')
            i += 1
            ## Unpack everything
            tile = sbid_info[0][7:]
            sbid = sbid_info[1][7:].split('.')[0] ## Remove trailing ".0"
            beamno = sbid_info[2][10:]
            beamsep = sbid_info[3][12:]
            ## Save all information
            band2_list.append([band, src_name, tile, sbid, beamno, beamsep])
   band1_list = np.array(band1_list)
   band2_list = np.array(band2_list)
   
   
   ## Read from history file, separate by band
   if os.path.exists(output_path):
      hist_data = np.genfromtxt(output_path, skip_header=1, dtype=str, delimiter=',')
      if len(hist_data.shape) == 1:
         hist_data = np.array([hist_data])
      band1_hist = hist_data[hist_data[:,0] == '1']
      band2_hist = hist_data[hist_data[:,0] == '2']
   else:
      hist_data = np.array([])
      band1_hist = np.array([[None]*6])
      band2_hist = np.array([[None]*6])
   
   
   output_text = '🔮 POSSUM target-based tracking report 🔮\n'
   output_text += 'Input target list: '+args.file_path.split('/')[-1]+'\n\n'
   ## Go through each observed field, report if previously unobserved
   output_text += '1️⃣  ✅ New Band 1 observed targets:\n'
   any_observed_band1, any_observed_band2 = False, False ## Track if any has already been found as observed
   already_reported = np.array([[None, None]]) ## Save which source-SBID has already been reported
   for band1_obs in band1_list:
      if np.any(np.all(np.isin(band1_obs, band1_hist), axis=0)) == False:
         ## New observation covering a target, report!
         ## First check if the target has previously been observed in another SBID
         if np.all(np.isin(band1_obs[1:3], already_reported), axis=0) == False:
            ## Only report once per Source-SBID pair
            any_observed_band1 = True
            prev_obs = band1_hist[band1_hist[:,1] == band1_obs[1]]
            if len(prev_obs) == 0:
               prev_obs = 'N/A'
            else:
               prev_obs = ','.join(prev_obs[:,3])
            output_text += 'Src: '+band1_obs[1]+' | SBID: '+band1_obs[3]+' | Tile: '+band1_obs[2]+' | Prev. obs. SBID: '+prev_obs+'\n'
            already_reported = np.append(already_reported, [band1_obs[1:3]])
   if any_observed_band1 == False:
      output_text += '=-=-= None =-=-=\n'
   output_text += '\n'
   output_text += '2️⃣  ✅ New Band 2 observed targets:\n'
   already_reported = np.array([[None, None]]) ## Save which source-SBID has already been reported
   for band2_obs in band2_list:
      if np.any(np.all(np.isin(band2_obs, band2_hist), axis=0)) == False:
         ## New observation covering a target, report!
         ## First check if the target has previously been observed in another SBID
         if np.all(np.isin(band1_obs[1:3], already_reported), axis=0) == False:
            any_observed_band2 = True
            prev_obs = band2_hist[band2_hist[:,1] == band2_obs[1]]
            if len(prev_obs) == 0:
               prev_obs = 'N/A'
            else:
               prev_obs = ','.join(prev_obs[:,3])
            output_text += 'Src: '+band2_obs[1]+' | SBID: '+band2_obs[3]+' | Tile: '+band2_obs[2]+' | Prev. obs. SBID: '+prev_obs+'\n'
            already_reported = np.append(already_reported, [band1_obs[1:3]])
   if any_observed_band2 == False:
      output_text += '=-=-= None =-=-=\n'
   output_text += '\n'


   ## Now go through previously observed fields, and make sure they are still listed as observed
   any_removed_band1, any_removed_band2 = False, False ## Track if any has already been found as removed
   for band1_obs in band1_hist:
      if np.all(band1_obs == np.array([[None]*6])):
         pass ## No previous observations --- skip
      elif np.any(np.all(np.isin(band1_obs, band1_list), axis=0)) == False:
         if any_removed_band1 == False:
            output_text += '1️⃣  ‼️  Removed Band 1 observed target:\n'
            any_removed_band1 = True
         output_text += 'Src: '+band1_obs[1]+' | Removed SBID: '+band1_obs[3]+' | Tile: '+band1_obs[2]+'\n'
   if any_removed_band1 == True:
      output_text += '\n'
   for band2_obs in band2_hist:
      if np.all(band2_obs == np.array([[None]*6])):
         pass ## No previous observations --- skip
      elif np.any(np.all(np.isin(band2_obs, band2_list), axis=0)) == False:
         if any_removed_band2 == False:
            output_text += '2️⃣  ‼️  Removed Band 2 observed target:\n'
            any_removed_band2 = True
         output_text += 'Src: '+band2_obs[1]+' | Removed SBID: '+band2_obs[3]+' | Tile: '+band2_obs[2]+'\n'
   if any_removed_band2 == True:
      output_text += '\n'

   ## Write new history file in .CSV format
   f = open(output_path, 'w')
   f.write('#band,src,tile,sbid,beamno,beamsep\n')
   for entry in band1_list:
      f.write(entry[0]+','+entry[1]+','+entry[2]+','+entry[3]+','+entry[4]+','+entry[5]+'\n')
   for entry in band2_list:
      f.write(entry[0]+','+entry[1]+','+entry[2]+','+entry[3]+','+entry[4]+','+entry[5]+'\n')
   f.close()

   for out_channel in out_channel_list:
      if out_channel == 'terminal':
         ## Print out results --- either to Terminal (as test), or via Slack bot
         ## In other words: Edit below if you want the results reported in some other ways
         print(output_text)
      else:
         ## Below for posting on Slack
         slack_token = os.environ['SLACK_TOKEN']
         from slack_sdk import WebClient
         client = WebClient(token=slack_token)
      
         client.chat_postMessage(
            channel=out_channel, 
            text=output_text, 
            username="POSSUM Source Tracker"
         )



if __name__ == '__main__':
   parser = argparse.ArgumentParser(description=docstring, formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument('file_path', type=str, help='Path to the text file containing coordinates in each row.')
   parser.add_argument('-o', '--output', type=str, help='Output CSV file used to track which targets have previously been observed')
   parser.add_argument('-c', '--channel', type=str, help='Destination Slack channel name. Use member ID for Slack DM. Use "terminal" for output to Unix terminal. For sending to multiple channels, provide a comma-separated list (e.g. -c channel1,channel2)')
      
   args = parser.parse_args()
   main(args)




