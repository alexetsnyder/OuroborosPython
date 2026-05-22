from enum import Enum

class Voxels(Enum):
    AIR = b'\x00'
    DIRT = b'\x01'
    GRASS = b'\x02'
    STONE = b'\x03'
    BEDROCK = b'\x04'

VoxelRow = [Voxels.AIR, Voxels.AIR, Voxels.AIR, Voxels.GRASS, Voxels.DIRT, Voxels.DIRT, Voxels.STONE, Voxels.STONE, Voxels.STONE, Voxels.BEDROCK]

def encode(VoxelRow):
    EncodedRow = []
    
    currentVoxel = VoxelRow[0]
    currentRun = 1
    for i in range(1, len(VoxelRow)):
        nextVoxel = VoxelRow[i]
        if (currentVoxel == nextVoxel):
            currentRun+=1
        else:
            EncodedRow.append(currentRun.to_bytes(1) + currentVoxel.value)
            currentRun = 1
            currentVoxel = nextVoxel
            
    EncodedRow.append(currentRun.to_bytes(1) + currentVoxel.value)
            
    return EncodedRow

def getVoxel(value):
    match value:
        case Voxels.AIR.value:
            return Voxels.AIR
        case Voxels.DIRT.value:
            return Voxels.DIRT
        case Voxels.GRASS.value:
            return Voxels.GRASS
        case Voxels.STONE.value:
            return Voxels.STONE
        case Voxels.BEDROCK.value:
            return Voxels.BEDROCK

def decode(EncodedRow):
    VoxelRow = []
    
    for i in range(len(EncodedRow)):
        value = int.from_bytes(EncodedRow[i])
        for j in range((value >> 8) & 0xFF):
            voxel = value & 0xFF
            VoxelRow.append(getVoxel(int.to_bytes(voxel)))
    
    return  VoxelRow
    
def indexVoxel(EnodedRow, index):
    runLength = 0
    for i in range(len(EncodedRow)):
        value = int.from_bytes(EncodedRow[i])
        count = (value >> 8) & 0xFF
        runLength += count
        if runLength > index:
            return getVoxel(int.to_bytes(value & 0xFF))

if __name__ == '__main__':
    EncodedRow = encode(VoxelRow)
    
    print(EncodedRow)
    
    print()
    print(indexVoxel(EncodedRow, 5))
    print()
    
    DecodedRow = decode(EncodedRow)
    
    print(DecodedRow)