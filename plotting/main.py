import numpy as np
import pandas as pd
import os

from utils import *



if __name__ == "__main__":
    #filePath= "./data/d3 it -1v 1.csv"
    #df, xlab, ylab= load_csv(filePath)
    #plot_loss_function(df.iloc[:,0], df.iloc[:,1], xlab, ylab, "IT")
    ivdir_path = "./IVdata"
    itdir_path = "./ITdata"
    intdir_path = "./Intdata"
    # data1, xlabel,ylabel,consistancy=multLoadCSV(ivdir_path)
    # IVX=[rf"Voltage (V)", rf"Voltage (V)"]
    # IVY= [rf"Current (A)", rf"Current (A)"]
    # legend_names=[r"$I_{off}$", r"$I_{on}$"]
    # title_list=[rf"I-V Curve Without Illumination", rf"I-V Curve With Illumination"]
    # line_plot_res(
    #     title_list,
    #     legend_names,
    #     data1,
    #     IVX,
    #     IVY,
    #     "IV curves",
    #     "IVs",
    #     consistancy,
    #     subplot=0,
    #     legend_order=None,
    #     ylog=False,
    #     xlog=False,
    # )
    # line_plot_res(
    #     title_list,
    #     legend_names,
    #     data1,
    #     IVX,
    #     IVY,
    #     "IV curves",
    #     "IVs2",
    #     consistancy,
    #     subplot=1,
    #     legend_order=None,
    #     ylog=False,
    #     xlog=False,
    # )
    
    # meas,xlab,ylab,const= measurement (data1[1],data1[0] , 0.4, 0.00257)
    # measX=[rf"Voltage (V)", rf"Voltage (V)",rf"Voltage (V)"]
    # measY= [rf"Photocurrent (A)", r"Responsivity ($\frac{A}{W}$)", rf"Specific Detectivity (Jones)" ]
    # leg= [r"$I_{ph}$", rf"Responsivity", rf"Detectivity"]
    # titles=[r"$I_{ph}$", rf"Responsivity",rf"Detectivity"]
    # line_plot_res(
    #     titles,
    #     leg,
    #     meas,
    #     measX,
    #     measY,
    #     "Measurements",
    #     "measurements",
    #     const,
    #     subplot=1,
    #     legend_order=None,
    #     ylog=False,
    #     xlog=False,
    # )
    

    # data2, xlabel2,ylabel2,consistancy2=multLoadCSV(itdir_path)
    # data2 = [df.iloc[3500:] for df in data2]
    # ITX=[rf"Time (s)", rf"Time (s)", rf"Time (s)",rf"Time (s)",rf"Time (s)"]
    # ITY= [rf"Current (A)", rf"Current (A)", rf"Current (A)", rf"Current (A)", rf"Current (A)"]
    # legend_n=[rf"0V",rf"1.5V",rf"1V",rf"2V",rf"0.5V" ]
    # ITtitle=[rf"I-T Curve for 0V Bias",rf"I-T Curve for 1.5V Bias", rf"I-T Curve for 1V Bias",rf"I-T Curve for 2V Bias",rf"I-T Curve for 0.5V Bias"]
    # line_plot_res(
    #     ITtitle,
    #     legend_n,
    #     data2,
    #     ITX,
    #     ITY,
    #     "IT curves",
    #     "ITs",
    #     consistancy2,
    #     subplot=1,
    #     legend_order=None,
    #     ylog=False,
    #     xlog=False,
    # )
    # line_plot_res(
    #     ITtitle,
    #     legend_n,
    #     data2,
    #     ITX,
    #     ITY,
    #     "IT curves",
    #     "ITs2",
    #     consistancy2,
    #     subplot=0,
    #     legend_order=[0,4,2,1,3],
    #     ylog=False,
    #     xlog=False,
    # )

    #data3, xlabel3,ylabel3,consistancy3=multLoadCSV(itdir_path)
    

    data3, xlabel3,ylabel3,consistancy3=intload()
    intensity_lvls=[3,4,5,6,7,8,9,10]
    powers= [185e-6,0.433e-3, 0.816e-3, 1.188e-3, 1.61e-3, 1.9e-3,2.173e-3,2.57e-3]
    res= process_all_datasets(data3,                              
                            intensity_levels=intensity_lvls,
                            ma_window=51,
                            steady_window=200,
                            steady_rel_std_threshold=0.02,
                            peak_prominence=None,   # or a number in same units as current
                            peak_distance=None,     # or set based on samples per period
                            prefer_anchors='peaks',
                            debug_plot=False)
    ioff = res["troughs"].apply(np.mean).to_numpy(dtype=float)
    resp=responsivity_array(res["ptp_mean"], powers,0.4)
    det=detectivity_array(resp, 0.4, ioff, tiny_ioff_threshold=1e-30)   

    pd_iph = np.column_stack((powers, res["ptp_mean"]))
    pd_responsivity = np.column_stack((powers, resp))
    pd_detectivity = np.column_stack((powers, det))
    df_iph = pd.DataFrame(pd_iph, columns=["Power", "Iph"])
    df_responsivity = pd.DataFrame(pd_responsivity, columns=["Power", "Responsivity"])
    df_detectivity = pd.DataFrame(pd_detectivity, columns=["Power", "Detectivity"])

    meas=[df_iph,df_responsivity,df_detectivity]
    measX=[r"Intensity ($\frac{W}{cm^{2}}$)", r"Intensity ($\frac{W}{cm^{2}}$)",r"Intensity ($\frac{W}{cm^{2}}$)"]
    measY= [rf"Photocurrent (A)", r"Responsivity ($\frac{A}{W}$)", rf"Specific Detectivity (Jones)" ]
    leg= [r"$I_{ph}$", rf"Responsivity", rf"Detectivity"]
    titles=[r"$I_{ph}$", rf"Responsivity",rf"Detectivity"]
    line_plot_res(
        titles,
        leg,
        meas,
        measX,
        measY,
        "Measurements",
        "meas",
        consistancy3,
        subplot=1,
        legend_order=None,
        ylog=False,
        xlog=False,
    )

