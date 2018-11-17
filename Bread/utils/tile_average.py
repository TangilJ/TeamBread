from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from Bread.bot_math.Vector3 import Vector3


def get_tile_average(packet: GameTickPacket, field_info: FieldInfoPacket) -> Vector3:
    num_tiles = 70  # Don't hard code this. It was like this because it was giving errors.
    sum_x = 0
    sum_y = 0
    sum_z = 0
    total_weight = 0
    weight_multiplier = 2  # tested 2 and 3, 2 seems better
    
    for num_tile in range(num_tiles):
        tile_weight = packet.dropshot_tiles[num_tile].tile_state ** weight_multiplier
        tile_x = field_info.goals[num_tile].location.x * tile_weight
        tile_y = field_info.goals[num_tile].location.y * tile_weight
        tile_z = field_info.goals[num_tile].location.z * tile_weight

        sum_x += tile_x
        sum_y += tile_y
        sum_z += tile_z
        total_weight += tile_weight

    median_x = sum_x / total_weight
    median_y = sum_y / total_weight
    median_z = sum_z / total_weight

    return Vector3(median_x, median_y, median_z)
