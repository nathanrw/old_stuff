def project_polygon(polygon, camera_size, camera_dist):
    newpoints = []
    for point in polygon.points:
        newpoints.append(project_point(point, camera_size, camera_dist))
    polygon.points = newpoints

def project_point(xyz, camera_size, camera_dist):
    
    a = camera_dist/(xyz[2]+0.00001)
    
    return (a * xyz[0] + camera_size[0] * 0.5,
            a * xyz[1] + camera_size[1] * 0.5)

if __name__ == '__main__':
    print project_point([10,10,330],[640,480],320)