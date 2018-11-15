

depth=$(ps -aux |grep python|grep huobi_websocket_depth_producer.py)
#echo $depth
#echo ${#depth}

#ticker=$(ps -aux | grep python | grep restapi_huobi_ticker.py)
#echo $ticker

trader=$(ps -aux|grep python|grep huobi_websocket_trade_producer.py)
#echo $trader

kline=$(ps -aux | grep python | grep huobi_websocket_kline_producer.py)
#echo $kline

#ntest=$(ps -aux | grep python | grep test.py)
#echo $ntest

#echo ${#ntest}
if [ ${#depth} -eq 0 ]
then
    echo "depth program close! start it "
    #source /home/yanjiuyuan/anaconda2/bin/activate python3
    nohup /root/anaconda3/bin/python /yanjiuyuan/code/huobi/src/huobi_websocket_depth_producer.py > /yanjiuyuan/code/huobi/log/depth.log 2>&1 &
    
fi

if [ ${#trader} -eq 0 ]
then
    echo "trader program close! start it"
    #source /home/yanjiuyuan/anaconda2/bin/activate python3
    nohup /root/anaconda3/bin/python /yanjiuyuan/code/huobi/src/huobi_websocket_trade_producer.py > /yanjiuyuan/code/huobi/log/trade.log 2>&1 &
fi

if [ ${#kline} -eq 0 ]
then
    echo "kline program close! start it"
    #source /home/yanjiuyuan/anaconda2/bin/activate python3
    nohup /root/anaconda3/bin/python /yanjiuyuan/code/huobi/src/huobi_websocket_kline_producer.py > /yanjiuyuan/code/huobi/log/kline.log 2>&1 &
fi

#if [ ${#ntest} -eq 0 ]
#then
#    echo "ntest program close! start it"
#    python /home/yanjiuyuan/huobi_demo/src/test.py > /home/yanjiuyuan/test.log

#fi
