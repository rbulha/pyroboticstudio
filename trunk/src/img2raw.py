'''
Created on 27/01/2011

@author: rogerio_bulha
'''

import struct

class CIMGSUPPORT(object):
    '''
    classdocs
    '''
    @staticmethod
    def BMP2RAW(file_name):
        bmp_file_path = '..\\data\\'+file_name
        try:
            bmp_file = open(bmp_file_path,'rb')
        except IOError:
            print 'falha em abrir o arquivo'
        else:
            image_raw = {}
            file_header = struct.unpack('27H',bmp_file.read(54))
            print 'HEADER:',file_header
            print 'SIZE(%d,%d)'%(file_header[9],file_header[11])
            image_raw['WIDTH'] = file_header[9]
            image_raw['HEIGHT']= file_header[11]
            total_size = file_header[9]*file_header[11]
            points_list = []
            for index in range(total_size):
                points_list.append(struct.unpack('BBB',bmp_file.read(3)))
            image_raw['DATA'] = points_list    
            return image_raw     

if __name__ == '__main__':
        image_raw = CIMGSUPPORT.BMP2RAW('pista_2.bmp')    
        print 'DATA(0):',image_raw['DATA'][0]
        print 'DATA(30):',image_raw['DATA'][30]        