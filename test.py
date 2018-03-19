import pyshark
import sys, os

frame_cnt = 0

def get_summary_info(pkt):
    global frame_cnt
    frame_cnt += 1
    try:
        eth_src = pkt.layers[0].src
        eth_dst = pkt.layers[0].dst
        ip_src = pkt.layers[1].src
        ip_dst = pkt.layers[1].dst
        tcp_srcport = pkt.layers[2].srcport
        tcp_dstport = pkt.layers[2].dstport

        print "#{0} {1} ({2}) {3} ----> {4} ({5}) {6}".format(frame_cnt, ip_src, eth_src, tcp_srcport, ip_dst, eth_dst, tcp_dstport)
    except:
        pass

class Extractor():
    def __init__(self):
        pass
    def extract_from_pcap(self, capturefile):
        cap = pyshark.FileCapture(capturefile)
        cap.apply_on_packets(get_summary_info, timeout=100)

def main():
    if len(sys.argv) < 2:
        print "Usage python pktAnalyzer.py capturefile "
        sys.exit()
    else:
        captureFile = str(os.path.abspath(sys.argv[1]))
    
    extractor = Extractor()
    extractor.extract_from_pcap(captureFile)
    

if __name__ == '__main__':
    main()
