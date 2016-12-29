#!/usr/bin/python
# this will only deal with IPv4 at the moment 

#imports
import socket
import struct
import binascii
import os
# for reference: 
'''
0 = 0000
f = 1111
3 = 001 
'''

def analyze_tcp_header(data):
	tcp_header = struct.unpack("!2H2I4H", data[:20])
	scr_port = tcp_header[0]
	dest_port = tcp_header[1]
	seq_num = tcp_header[2] # SYN
	ack_num = tcp_header[3] # ACK
	data_offset = tcp_header[4] >> 12 
	reserved = (tcp_header[4] >> 6) & 0x03ff # MUST BE 0 
	flags = tcp_header[4] & 0x003f
	window = tcp_header[5]
	chk_sum = tcp_header[6]
	urg_pointer = tcp_header[7]
	data = data[20:]
	
	urg = bool(flags & 0x0020)
	ack = bool(flags & 0x0010)
	psh = bool(flags & 0x0008)
	rst = bool(flags & 0x0004)
	syn = bool(flags & 0x0002)
	fin = bool(flags & 0x0001)
	
	print "|==============TCP HEADER==============|"
	print "|\tSource:\t\t%hu" % scr_port
	print "|\tDest:\t\t%hu" % dest_port
	print "|\tSYN:\t\t%u" % seq_num
	print "|\tACK:\t\t%u" % ack_num
	print "|\tFlags\t\t: "
	print "|\tURG:%d" % urg
	print "|\tACK:%d" % ack
	print "|\tPSH:%d" % psh
	print "|\tRST:%d" % rst
	print "|\tSYN:%d" % syn
	print "|\tFIN:%d" % fin
	print "|\tWindow:\t\t%hu" % window
	print "|\tChecksum:\t\t%hu" % chk_sum
	print "|\tURG POINTER:\t\t%hu" % urg_pointer
	
	return data
	
def analyze_udp_header(data):
	udp_header = struct.unpack("!4h"), data[:8])
	scr_port = udp_header[0]
	dst_port = udp_header[1]
	length = udp_header[2]
	chk_sum = udp_header[3]
	data = data[8:]
	
	print "|==============UDP HEADER==============|"
	print "|\tSource:\t\t%hu" % scr_port
	print "|\tDest:\t\t%hu" % dst_port
	print "|\tLength:\t\t%hu" % length
	print "|\tChecksum:\t\t%hu" % chk_sum
	
	return data
	
def analyze_ip_header(data):
	# IPv4 RFC as source
	ip_header = struct.unpack("!5H4s4s", data[:20])
	ver = ip_header[0] >> 12 # shift 12 bits moving version
	ihl = (ip_header[0] >> 8) & 0x0f 
	tos = ip_header[0] & 0x00ff # type of service
	tot_len = ip_header[1] # total length
	ip_id = ip_header[2]
	flags = ip_header[3] >> 13 # only gets first 3 bits of flags
	ip_ttl = ip_header[4] >> 8
	ip_proto = ip_header[4] & 0x00ff
	chk_sum = ip_header[5]
	frag_offset = ip_header[3] & 0x1fff
	src_addr = socket.inet_ntoa(ip_header[6])
	dest_addr = socket.inet_ntoa(ip_header[7])
	# check the protocols again check for TCP and UPD
	# TODO ADD MQTT
	
	print "|==============IP HEADER==============|"
	print "\tVersion:\t%hu" % ver
	print "\tIHL:\t\t%hu" % ihl
	print "\tTOS:\t\t%hu" % tos
	print "\tLength:\t\t%hu" % tot_len
	print "\tID:\t\t%hu" % ip_id
	print "\tOffset:\t\t%hu" % frag_offset
	print "\tTTL:\t\t%hu" % ip_ttl
	print "\tNext Proto:\t\t%hu" % ip_proto
	print "\tChecksum:\t\t%hu" % chk_sum
	print "\tSource IP:\t\t%s" % src_addr
	print "\tDest IP:\t\t%s" % dest_addr
	
	if ip_proto == 6: 
		next_proto = "TCP"
	elif ip_proto = 17:
		next_proto = "UDP"
	else: 
		next_proto = "OTHER"
	
	data = data[20:]
	 
	return data, next_proto
	

def analyze_data_header(data):
	ip_bool = False
	
	# the header starts with the mac address so set to 6 bytes
	'''6s mac dest, 6s mac source, H eathertype un-signed short'''
	eth_header    = struct.unpack("!6s6sH", data[:14]) #IPv4 = 0x0800
	# eth_header is coming back as a touple so break it out
	dest_mac_addr = binascii.hexlify(eth_header[0]) #Destionation Address
	src_mac_addr  = binascii.hexlify(eth_header[1]) #Source Address
	proto		  = eth_header[2] >> 8 #Next Protocol
	
	#print out so a human can understand it
	print "|==============ETH HEADER==============|"
	print "|Destination MAC Addr:\t %s:%s:%s:%s:%s:%s:" % (dest_mac_addr[0:2],dest_mac_addr[2:4],
	dest_mac_addr[4:6], dest_mac_addr[6:8], dest_mac_addr[8:10], dest_mac_addr[10:12])
	
	print "|Source MAC Addr:\t\t %s:%s:%s:%s:%s:%s:" % (src_mac_addr[0:2],src_mac_addr[2:4],
	src_mac_addr[4:6], src_mac_addr[6:8], src_mac_addr[8:10], src_mac_addr[10:12])
	
	print "|Proto: %s:\t\t " % hex(proto)
	
	if hex(proto) == '0x0800':
		ip_bool = True
		
	
	data = data[:14] # strip out what you do not need
	return data, ip_bool
	
def main():
	# as is setting to get raw packet, and ETH_P_ALL give me everything
	sniffer_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0X0003))
	# DO NOT BIND a raw socket, as it is not going on a specific port
	# if you set it then its only going to listen on that port
	recv_data = sniffer_socket.recv(2048) # <== comes back as a struct 
	# clear out the data
	os.system("clear") # will work on linux
	data , ip_bool = analyze_data_header(recv_data)
	
	if ip_bool: 
		data, next_proto = analyze_data_header(data)
	else: 
		return
	
	if next_proto == "TCP":
		data = analyze_tcp_header(data)
	elif next_proto == "UDP":
		data = analyze_udp_header(data)
	else: 
		return
		
main()
