from read_write_geotiff import read_tif, array_to_geotiff

array, transform, projection, rows, cols = read_tif("data/imagery.tif")
if array.ndim == 2:
    array = array[..., None]
array_to_geotiff(array, "data/imagery_copy.tif", transform, projection)
print(rows, cols, array.shape)
