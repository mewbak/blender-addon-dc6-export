def biglong(n, bytecount=4):
    # 0x12345678 -> [0x12, 0x34, 0x56, 0x78]
    return [(n&(0xff<<(8*i)))>>(8*i) for i in range(bytecount)]

class DC6FileHeader:
    def __init__(self, directions, frames):
        self.terminator = 0xEE
        self.version    = 6
        self.unknown01  = 1
        self.unknown02  = 0
        self.directions = directions
        self.frames     = frames
    
    def getbytes(self):
        b = bytearray()
        b.extend(biglong(self.version))
        b.extend(biglong(self.unknown01))
        b.extend(biglong(self.unknown02))
        b.extend([self.terminator]*4)
        b.extend(biglong(self.directions))
        b.extend(biglong(self.frames))
        return b

class DC6FrameHeader:
    def __init__(self, width, height, length=0, offsetx=0, offsety=0, flip=False):
        self.width      = width
        self.height     = height
        self.offsetx    = offsetx
        self.offsety    = offsety
        self.flip       = flip
        self.length     = length
        self.nextblock  = 0
    
    def getbytes(self):
        b = bytearray()
        b.extend(biglong(self.flip))
        b.extend(biglong(self.width))
        b.extend(biglong(self.height))
        b.extend(biglong(self.offsetx))
        b.extend(biglong(self.offsety))
        b.extend(biglong(0)) # unknown
        b.extend(biglong(self.nextblock))
        b.extend(biglong(self.length))
        return b

class DC6FrameData:
    def __init__(self, width, height, data, alpha_index=0, flip=False):
        self.width          = width
        self.height         = height
        self.data           = data
        self.alpha_index    = alpha_index
        self.flip           = flip
    
    def getbytes(self):
        return self._encode(self.data)
    
    def _encode(self, data):
        w = self.width
        rows = [data[n:n+w+1] for n in range(len(data))[::w]]
        
        if self.flip<1:
            rows = rows[::-1]
        
        encoded = bytearray(0)
        for row in rows:
            encoded.extend(self._encode_scanline(row, self.alpha_index))
        return encoded
    
    def _encode_scanline(self, data, alpha_index=0):
        encoded = bytearray()
        groups = self._group_bytes_by_alpha(data, alpha_index)
        
        for group in groups:
            group_bytes = bytearray()
            if alpha_index in group:
                if group != groups[-1]:
                    group_bytes.extend([0x80|len(group)])
            else:
                group_bytes.extend([0x7F&len(group)])
                group_bytes.extend(group)
            encoded.extend(group_bytes)
        encoded.extend([0x80])
        return encoded
    
    def _group_bytes_by_alpha(self, data, alpha=0):
        encoded = bytearray
        current = data[0]
        is_alpha = current == alpha
        groups = [[current]]
        for data_index in range(1, len(data)):
            current = data[data_index]
            contiguous = (current == alpha) == is_alpha
            if not contiguous:
                is_alpha ^= 1
                groups.append([current])
            else:
                group = groups[len(groups)-1]
                if len(group) < 0x80:
                    group.append(current)
                else:
                    groups.append([current])
        return groups

class DC6Frame:
    def __init__(self, width, height, data, alpha_index=0):
        self.header = DC6FrameHeader(width, height)
        self.framedata = DC6FrameData(width, height, data, flip=self.header.flip)
    
    def getbytes(self):
        b = bytearray()
        data = self.framedata.getbytes()
        self.header.length = len(data)
        b.extend(self.header.getbytes())
        b.extend(data)
        return b
    

class DC6FileEncoder:
    """A DC6 image file used in Diablo II"""
    def __init__(self, num_directions, num_frames, width, height, framedatas, alpha_index=0):
        self.header = DC6FileHeader(num_directions, num_frames)
        self.frames = [DC6Frame(width, height, data) for data in framedatas]
    
    def fileinfo(self):
        print('Version: %d' % self.header.version)
        if self.header.version != 6:
            print("WARNING: version should be '6'")
        print('Directions: %d' % self.header.directions)
        print('Frames per direction: %d' % self.header.frames)
        print('Number of frames: %d' % (self.header.directions * self.header.frames) )
        print('Animated: %s' % ['False', 'True'][self.header.frames>1])
    
    def getpointers(self):
        b = bytearray()
        numpointers = self.header.directions * self.header.frames
        start = len(self.header.getbytes()) + (numpointers*4) # each pointer is 32-bit
        offset = start
        b.extend(biglong(offset))
        for frame in self.frames[:-1]: # dont need the last one
            framelength = len(frame.getbytes())
            offset += framelength
            b.extend(biglong(offset))
        return b
    
    def getbytes(self):
        b = bytearray()
        b.extend(self.header.getbytes())
        b.extend(self.getpointers())
        for frame in self.frames:
            b.extend(frame.getbytes())
            b.extend([self.header.terminator]*3)
        return b

