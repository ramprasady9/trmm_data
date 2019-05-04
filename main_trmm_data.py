#!/usr/bin/python3
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as pp
import pandas as pd

import datetime

def read_trmm_nc4(ifilename,ires):
    
    ds = Dataset(ifilename,'r',format='NETCDF4') 
    # Dataset is the class behavior to open the file
    # and create an instance of the ncCDF4 class

    # print(ds.file_format)
    # print(ds.variables)
    # print(ds.groups)
    # print(ds.dimensions)
    
    lon=np.array(ds.variables['lon'])
    lat=np.array(ds.variables['lat'])
    data2d=np.array(ds.variables['precipitation'])
    ds.close()
    if ires=='1d':
        data1d=np.reshape(data2d,(1,1440*400))
        return {'lon': lon, 'lat': lat ,'data1d': data1d}
    else:
        if ires=='2d':
            return {'lon': lon, 'lat': lat ,'data2d': data2d}
        else:
            print('Error: Invalid input,required inputs are 1d or 2d\n')
            return 0

## function for getting grid points across globe based on sample trmm_data provided        
def trmm_get_gridpoints(trmm_data):
    ## sno,lon,lat,ilon,ilat 
    gpoints=np.full((trmm_data['lon'].size*trmm_data['lat'].size,5),0.0,dtype=np.float32)
    # Because python needs zero based indexing
    ir=0
    iy=0

    for y in np.nditer(trmm_data['lat']):
        ix=0
        for x in np.nditer(trmm_data['lon']):
            if ir%10000==0:
                print(ir)
                
            gpoints[ir,0]=ir+1
            gpoints[ir,1]=x
            gpoints[ir,2]=y
            gpoints[ir,3]=ix
            gpoints[ir,4]=iy
            ir=ir+1
            ix=ix+1
        iy=iy+1
            # break

def trmm_write_grid2csv(trmm_data):
    gpoints=trmm_get_gridpoints(trmm_data)
    np.savetxt("global_trmm_points.csv", gpoints, delimiter=",",fmt='%d,%.3f,%.3f,%d,%d')
    return gpoints

## plotting data of different grid points of precipitation
## this function was originally written to test conversion of 
## 2d array precipitation to 1D array format-> may not be useful later
def plot_row(trmm_data,i):
    ## i starts with 1
    # precip1=np.reshape(trmm_data['data2d'],(1,1440*400))
    precip1=trmm_data['data1d']
    ## 1 -> 0 :399
    ## 2 -> 400 : 799
    ## 3 -> 800 : 1199
    nrow=400
    # ncol=1440 -> not used
    # % matplotlib inline
    pp.plot(precip1[0,((nrow)*(i-1)):((nrow)*(i-1)+nrow)],'g',linewidth=0.2,marker='o',label='1d precip')
    # pp.plot(trmm_data['data2d'][i-1,0:(nrow-1)],'r',linewidth=0.5,label='2d precip')
    pp.grid(axis='both')
    pp.xlabel('Time in (days)')
    pp.ylabel('Precipitation in (mm)')
    pp.title('Different grid points precipitation')
    pp.legend()
    pp.show()
    return 0

def plot_grid_rain(rain_data,listdates,i):
    # pp.plot(rain_data[i,:],'b',label='precip')
    pp.bar(listdates,rain_data[i,:],color='skyblue',label='precip')
    # pp.grid(axis='both')
    pp.xlabel('Time in (days')
    pp.ylabel('Precipitation in (mm)')
    pp.title('grid point precipitation')
    pp.legend()
    pp.show()
    return 0


def get_trmm_dates_all():
    # today=datetime.date.today()
    startDay=datetime.date(1998,1,1)
    endDay=datetime.date(2014,12,31)
    
    delta=endDay-startDay # +1
    # delta.days+1
    # print(delta.days)
    listdates=[]
    for i in range(delta.days + 1):
        iday=startDay + datetime.timedelta(i)
        listdates.append(datetime.date.strftime(iday,'%Y%m%d'))
    # print(listdates)
    return listdates

def get_trmm_dates_all_python():
    # today=datetime.date.today()
    startDay=datetime.date(1998,1,1)
    endDay=datetime.date(2014,12,31)
    
    delta=endDay-startDay # +1
    # delta.days+1
    print(delta.days)

    dd = [startDay + datetime.timedelta(days=x) for x in range((endDay-startDay).days + 1)]      
    lmonth=[]
    
    for x in dd:
        lmonth.append(x.month+x.year*100)
    return lmonth

def get_trmm_data_by_country(pathIn,icountry):
    listdates=get_trmm_dates_all()
    # TRMM data version last available as of 21st April 2019 for download
    # pathIn = '/run/media/ram/Work/trmm_data/'
    ## reading grip points list
    trmm_gridp_csv=pathIn + 'trmm_points_by_countryjoin.csv'
    df_grid = pd.read_csv(trmm_gridp_csv)
    
    ## filtering based on country
    df_grid_country=df_grid[ df_grid['NAME']==icountry]
    # print(df_grid_country['index'].head())
    print(df_grid_country.size )
    # print(len(listdates))
    
    data=np.full((df_grid_country['index'].size,len(listdates)),0.0,dtype=np.float32)
    
    trmm_data_version=str(7)
    iday=0
    for x in listdates:
        nc_file=pathIn+ 'precip/' + '3B42_Daily.'+ x + '.'+trmm_data_version +'.nc4'
        print(x)
        trmm_data=read_trmm_nc4(nc_file,ires = '1d')
        data[:,iday]=trmm_data['data1d'][0,df_grid_country['index']];
        iday=iday+1
    return {'listdates': listdates,'index': df_grid_country['index'],'ilon': df_grid_country['ilon'],'ilat' :df_grid_country['ilat'],'lon': df_grid_country['lon'], 'lat': df_grid_country['lat'] ,'data': data}

## main function to test functions
def main():
    # sample TRMM rainfall file for nc4
    # PathIn needs to be the root folder for TRMM data, data are stored in netcdf4 format
    # Precipitation data is stored inside a folder 'Precip'
    pathIn = '/run/media/ram/Work/trmm_data/'
    res=get_trmm_data_by_country(pathIn,'Sri Lanka')
    listdates_int = list(map(int, res['listdates']))
    plot_grid_rain(res['data'],listdates_int,0)
    # trmm_grid=trmm_write_grid2csv(trmm_data)
    # plot_row(trmm_data,1200)

if __name__ == "__main__":
    main()
