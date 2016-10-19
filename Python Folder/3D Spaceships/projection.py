def project_polygons(polygons, camera_size, camera_dist):
    newpolies = []
    for poly in polygons:
        newpoints = []
        for point in poly.points:
            newpoints.append(project_point(point, camera_size, camera_dist))
        poly.points = newpoints

def project_point(xyz, camera_size, camera_dist):
    
    a = camera_dist/(xyz[2]+0.00001)
    
    return (a * xyz[0] + camera_size[0] * 0.5,
            a * xyz[1] + camera_size[1] * 0.5)
