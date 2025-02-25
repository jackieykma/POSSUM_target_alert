# POSSUM_target_alert

A script that checks the POSSUM observation status of a list of target sources

Once a new target has been observed, announce on the POSSUM Slack channel via Slack bot

Best to run this periodically (weekly?) via e.g. `cron`



## Installation

```
git clone https://github.com/jackieykma/POSSUM_target_alert.git
cd POSSUM_target_alert
git clone https://github.com/candersoncsiro/POSSUM.git
ln -s POSSUM/full_survey_band1_beam_center.csv ./full_survey_band1_beam_center.csv
ln -s POSSUM/full_survey_band2_beam_center.csv ./full_survey_band2_beam_center.csv
```
The above command downloads this `POSSUM_target_alert` script, as well as the `POSSUM` script maintained by Craig Anderson that this script depends on



## ...
