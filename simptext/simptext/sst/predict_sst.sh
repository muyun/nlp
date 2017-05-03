set -eu

IN=$1
model=sst.model

# prediction only

	python2.7 simptext/sst/src/main.py --cutoff 5 --YY simptext/sst/tagsets/bio2gNV --defaultY O --predict $IN --debug --load simptext/sst/$model --bio NO_SINGLETON_B --cluster-file simptext/sst/mwelex/yelpac-c1000-m25.gz --clusters 
	--lex simptext/sst/mwelex/{semcor_mwes,wordnet_mwes,said,phrases_dot_net,wikimwe,enwikt}.json
