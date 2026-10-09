import numpy as np
from osgeo import gdal, ogr, gdalconst

def read_tif(tif_file):
    """
    Parameters:
    ------------------------------
      - tif_file: the full path of the GeoTIFF data (e.g., "/data/imagery.tif").
      - im_data: (rows, cols, bands)
    """
    dataset = gdal.Open(tif_file)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    im_proj = (dataset.GetProjection())
    im_Geotrans = (dataset.GetGeoTransform())
    im_data = dataset.ReadAsArray(0, 0, cols, rows)
    if im_data.ndim == 3:
        im_data = np.moveaxis(dataset.ReadAsArray(0, 0, cols, rows), 0, -1)

    dataset = None
    return im_data, im_Geotrans, im_proj, rows, cols

def array_to_geotiff(array, output_path, geo_transform, projection, band_names=None):
    """
    Parameters:
    ------------------------------
      - array: the image array that need to be saved (rows, cols, bands).
      - output_path: the full path that save the GeoTIFF data (e,g., "/data/saved_imagery.tif").
      - geo_transform: geotransform of data.
      - projection: projection of data.
      - band_names: the band names as list.
    """
    rows, cols, num_bands = array.shape
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(output_path, cols, rows, num_bands, gdal.GDT_Float32)
    
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)
    
    for band_num in range(num_bands):
        band = dataset.GetRasterBand(band_num + 1)
        band.WriteArray(array[:, :, band_num])
        band.FlushCache()
        
        if band_names:
            band.SetDescription(band_names[band_num])
    dataset = None
    band = None
    return