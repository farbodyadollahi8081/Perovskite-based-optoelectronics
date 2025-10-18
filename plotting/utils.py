import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import ListedColormap
import pandas as pd
from scipy.constants import e
from scipy.signal import find_peaks




def load_csv(file_path):
    """
    Loads photodetector CSV file with metadata.
    Finds the row where first column == 'DataName',
    extracts x and y labels, and returns clean DataFrame.
    """
    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()
    
    # Find the row containing "DataName"
    header_row = None
    for i, line in enumerate(lines):
        if line.strip().startswith("DataName"):
            header_row = i
            break
    
    if header_row is None:
        raise ValueError("Could not find 'DataName' row in file.")
    
    # Get x and y axis labels
    parts = lines[header_row].strip().split(",")
    x_label, y_label = parts[1], parts[2]
    
    # Load the data after this row
    df = pd.read_csv(
        file_path,
        skiprows=header_row+1,  # start after the DataName row
        header=None,
        usecols=[1,2],          # take only 2nd and 3rd columns
        names=[x_label, y_label]
    )
    
    return df, x_label, y_label

def multLoadCSV(dir_path):

    # Get all CSV files in the directory
    file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]

    # Load and process all CSV files
    datasets = []
    x_labels = []
    y_labels = []

    for file_path in file_paths:
        data, x_label, y_label = load_csv(file_path)
        datasets.append(data)
        x_labels.append(x_label)
        y_labels.append(y_label)

    # Check if all x and y labels are consistent for a single plot
    consistancy=all(x == x_labels[0] for x in x_labels) and all(y == y_labels[0] for y in y_labels)

    return datasets, x_labels, y_labels, consistancy

def intload():
    i1="./Intdata/1V 3 F.csv"
    i2="./Intdata/1V 4 F.csv"
    i3="./Intdata/1V 5 F.csv"
    i4="./Intdata/1V 6 F.csv"
    i5="./Intdata/1V 7 F.csv"
    i6="./Intdata/1V 8 F.csv"
    i7="./Intdata/1V 9 F.csv"
    i8="./Intdata/1V 10 F.csv"

    d1,x1,y1=load_csv(i1)
    d2,x2,y2=load_csv(i2)
    d3,x3,y3=load_csv(i3)
    d4,x4,y4=load_csv(i4)
    d5,x5,y5=load_csv(i5)
    d6,x6,y6=load_csv(i6)
    d7,x7,y7=load_csv(i7)
    d8,x8,y8=load_csv(i8)
 
    datasets=[]
    x_labels = []
    y_labels = []
    datasets.append(d1)
    x_labels.append(x1)
    y_labels.append(y1)
    datasets.append(d2)
    x_labels.append(x2)
    y_labels.append(y2)
    datasets.append(d3)
    x_labels.append(x3)
    y_labels.append(y3)
    datasets.append(d4)
    x_labels.append(x4)
    y_labels.append(y4)
    datasets.append(d5)
    x_labels.append(x5)
    y_labels.append(y5)
    datasets.append(d6)
    x_labels.append(x6)
    y_labels.append(y6)
    datasets.append(d7)
    x_labels.append(x7)
    y_labels.append(y7)
    datasets.append(d8)
    x_labels.append(x8)
    y_labels.append(y8)


    consistancy=all(x == x_labels[0] for x in x_labels) and all(y == y_labels[0] for y in y_labels)

    return datasets, x_labels, y_labels, consistancy
#def moving_avg(arr, n):
 #   return np.convolve(arr, np.ones(n) / n, "same")
def moving_avg(arr, n):
    # Pad the beginning of the array with the first value
    arr=np.array(arr)
    padding = [arr[0]] * (n - 1)
    padded_arr = np.concatenate((padding, arr))
    # Apply convolution with 'valid' mode to avoid edge artifacts
    return np.convolve(padded_arr, np.ones(n) / n, "valid")

def line_plot_res(
    titles,
    legend_names,
    data1,
    xlabel,
    ylabel,
    title,
    fig_name,
    consistancy,
    subplot,
    legend_order=None,
    ylog=False,
    xlog=False,
):
    # Data for plotting

    # Positioning of bars on x-axis
    plt.rcParams["font.size"] = 36
    #plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["text.usetex"] = True
    #_ = range(len(alg_set))
    colors = ListedColormap(
        [
            "#ffbb78",  # Light orange
            "#17becf",  # Cyan
            "#2ca02c",  # Green
            "#d62728",  # Red
            "#1f77b4",  # Blue
            "#9467bd",  # Purple
            "#ff7f0e",  # Orange
            "#8c564b",  # Brown
            "#e377c2",  # Pink
            "#7f7f7f",  # Gray
            "#bcbd22",  # Yellow-green
            "#aec7e8",  # Light blue
        ]
    ).colors

    markers = ["o", "s", "D", "^", "v", "<", ">", "*", "+", "x", "p", "H"]

    do_unify= (not subplot) and consistancy
    # Plotting both tasksets
    os.makedirs("results", exist_ok=True)
    file_path = f"results/{fig_name}.png"

    if len(data1) == 1:
        do_unify = True
        print("Only one file detected. Switching to single plot despite subplot=True for better visualization.")

    if do_unify:

        fig = plt.figure(figsize=(30, 12))
        if ylog:
            plt.yscale("log")
        if xlog:
            plt.xscale("log")
        for i,data in enumerate(data1):
            color = colors[i%len(colors)]
            plt.plot(
                data.iloc[:,0].values,
                moving_avg(data.iloc[:,1].values,3),
                label=rf"{legend_names[i]}",
                color=color,
                linewidth=5,
                #marker=markers[-2],
                #markersize=1,
            )
        #plt.ylim(min(data1[0].iloc[:, 1].min() * 0.9, -1e-12), max(data1[0].iloc[:, 1].max() * 1.1, 1e-12))
        # Labels and Title
        plt.xlabel(rf"{xlabel[0]}")
        plt.ylabel(rf"{ylabel[0]}")
        plt.title(rf"{title}")

        if legend_order is None:
            _ = plt.legend()
        else:
            handles, labels = (
                plt.gca().get_legend_handles_labels()
            )  # Specify the order you want for the legend
            plt.legend(
                [handles[idx] for idx in legend_order],
                [labels[idx] for idx in legend_order],
            )

        plt.tight_layout()
        # Displaying the plot
        plt.grid(True)
        fig.savefig(file_path)
        plt.close(fig)
    else:
        n_plots=len(data1)
        fig,axes = plt.subplots(n_plots, 1, figsize= (30,12*n_plots), sharex=True)
        for i, (data, ax, xlab,ylab,titl) in enumerate(zip(data1,axes,xlabel, ylabel,titles)):
            color = colors[i%len(colors)]
            ax.plot(
                data.iloc[:,0],
                moving_avg(data.iloc[:,1],3),
                label=rf"{legend_names[i]}",
                color=color,
                linewidth=5,
                #marker=markers[-2],
                #markersize=1,
            )
            if ylog:
                ax.set_yscale("log")
            # Set logarithmic scale for x-axis if xlog is True
            if xlog:
                ax.set_xscale("log")
            ax.set_xlabel(rf"{xlab}")
            ax.set_ylabel(rf"{ylab}")
            ax.set_title(titl)
            #ax.set_ylim(data.iloc[:, 1].min() * 0.9, data.iloc[:, 1].max() * 1.1)
            if legend_order is None:
                _ = ax.legend()
            else:
                handles, labels = (
                    ax.get_legend_handles_labels()
                )  # Specify the order you want for the legend
                ax.legend(
                    [handles[idx] for idx in legend_order],
                    [labels[idx] for idx in legend_order],
                )
            ax.grid(True)
            ax.text(0.02, 0.98, f'({chr(97 + i)})', transform=ax.transAxes, 
                fontsize=40, fontweight='bold', va='top')
        
        fig.suptitle(f"{title}", fontsize=50, y=0.98)
        plt.tight_layout()
        fig.savefig(file_path)
        plt.close(fig)



def photocurrent(ION,IOFF):
    return ION-IOFF
        
def responsivity(IPH, diameter, power):
    return IPH/(np.pi*(diameter/2)**2 * power)     # diameter in cm and power in W/cm^2. IPH in A
        
def detectivity(responsivity, diameter, IOFF):
    return responsivity * np.sqrt(np.pi*(diameter/2)**2 / (2*e*np.abs(IOFF)))
        
def measurement(ion_df, ioff_df, diameter, power):
    """
    ion_df: DataFrame measured under light
    ioff_df: DataFrame measured in dark
    diameter: detector diameter (cm)
    power: light power density (W/cm^2)
    """
    # Ensure same length (truncate to shortest)
    n = min(len(ion_df), len(ioff_df))
    ion = ion_df.iloc[:n, 1]   # take second column (current)
    ioff = ioff_df.iloc[:n, 1]

    #   Compute parameters
    iph = photocurrent(ion, ioff)
    R = responsivity(iph, diameter, power)
    D = detectivity(R, diameter, ioff)

    # Build result DataFrame
    Iph = ion_df.iloc[:n, [0]].copy()   # keep time column
    Iph["Iph"] = iph.values
    response = ion_df.iloc[:n, [0]].copy()
    response["Responsivity"] = R.values
    detect = ion_df.iloc[:n, [0]].copy()
    detect["Detectivity"] = D.values
    xph="v1"
    yph="Iph"
    xr="v1"
    yr="Responsivity"
    xd="v1"
    yd="detectivity"
    x_labels =  [xph,xr,xd]
    y_labels= [yph,yr,yd]
    consistancy=all(x == x_labels[0] for x in x_labels) and all(y == y_labels[0] for y in y_labels)
    return [Iph,response, detect],x_labels, y_labels,consistancy



























def detect_steady_state_index(current, window=200, rel_std_threshold=0.02, min_index_frac=0.05):
    """
    Returns a start index for steady-state region.
    - current: 1D array (smoothed)
    - window: samples for rolling std
    - rel_std_threshold: threshold relative to current range
    - min_index_frac: minimum fraction of data to skip if detection fails
    """
    s = pd.Series(current)
    roll_std = s.rolling(window, center=True, min_periods=1).std().fillna(method='bfill').fillna(method='ffill').values
    crange = np.max(current) - np.min(current) + 1e-12
    rel_std = roll_std / crange

    # find first index where rel_std stays below threshold for a sustained region
    mask = rel_std < rel_std_threshold
    if mask.any():
        # require that following M samples also be True to avoid a single dip
        M = max(3, int(0.02 * len(current)))  # at least 3 samples or 2% of length
        # find first run of length >= M
        consec = 0
        for i, m in enumerate(mask):
            if m:
                consec += 1
            else:
                consec = 0
            if consec >= M:
                # steady region starts when this run began
                start_idx = i - consec + 1
                return max(start_idx, int(len(current) * min_index_frac))
    # fallback: cut first 20% (or min_index_frac if bigger)
    return int(len(current) * max(0.2, min_index_frac))

def find_cycles_using_peaks(current, min_distance=None, prominence=None):
    """
    Find peak indices and trough indices. Returns arrays (peaks, troughs).
    - min_distance in samples between peaks; if None a heuristic is used.
    - prominence helps to ignore noise-induced small peaks.
    """
    if min_distance is None:
        # heuristic: sample count / expected cycles ~ assume at least 5 cycles in trace
        min_distance = max(3, len(current) // 50)

    peaks, _ = find_peaks(current, distance=min_distance, prominence=prominence)
    troughs, _ = find_peaks(-current, distance=min_distance, prominence=prominence)
    return peaks, troughs

def compute_cycle_ptps_from_peaks_troughs(current, peaks, troughs, prefer='peaks'):
    """
    Using peaks or troughs to split cycles and compute peak-to-peak per cycle.
    prefer: 'peaks' or 'troughs' - indicates which anchor to use for cycle boundaries.
    Returns:
      - ptp_per_cycle: list of p2p values per cycle
      - cycle_boundaries: list of (start_idx, end_idx)
    Method:
      - If using 'peaks': cycles are between successive peaks; for each cycle find max and min inside that interval.
      - If using 'troughs': cycles between troughs similarly.
    """
    ptps = []
    bounds = []

    anchors = peaks if prefer == 'peaks' else troughs
    if len(anchors) < 2:
        return np.array(ptps), bounds

    for i in range(len(anchors)-1):
        s = anchors[i]
        e = anchors[i+1]
        seg = current[s:e+1]
        if seg.size > 2:
            ptp = seg.max() - seg.min()
            ptps.append(ptp)
            bounds.append((s, e))
    return np.array(ptps), bounds




def process_single_dataset(df,
                           time_col=0, current_col=1,
                           ma_window=51,
                           steady_window=200, steady_rel_std_threshold=0.02,
                           peak_prominence=None, peak_distance=None,
                           prefer_anchors='peaks',
                           debug_plot=False):
    """
    Process a single dataframe (time, current) and return:
      dict with keys:
        'ptp_mean' : mean peak-to-peak across cycles in steady-state
        'ptp_std'  : std of per-cycle ptp
        'ptp_cycles': array of per-cycle ptp
        'n_cycles' : number of cycles used
        'start_idx' : steady-state start index (in original array indices)
        'peaks' : peak indices (global)
        'troughs' : trough indices (global)
        'bounds' : cycle boundaries (list of (s,e) indices used)
    """
    time = df.iloc[:, time_col].values
    current_raw = df.iloc[:, current_col].values

    # 1) Smooth
    current_smooth = moving_avg(current_raw, n=ma_window)

    # 2) detect steady-state start
    start_idx = detect_steady_state_index(current_smooth, window=steady_window, rel_std_threshold=steady_rel_std_threshold)

    # only analyze steady-state portion
    current_ss = current_smooth[start_idx:]
    time_ss = time[start_idx:]

    # 3) find peaks and troughs in steady-state (indices are relative to steady-state array)
    # set reasonable defaults for peak detection
    if peak_distance is None:
        # assume at least 5 cycles -> distance ~ len_ss/5
        peak_distance = max(3, len(current_ss) // 10)
    if peak_prominence is None:
        # set to small fraction of signal range to ignore tiny bumps
        peak_prominence = (np.max(current_ss) - np.min(current_ss)) * 0.05

    peaks_rel, troughs_rel = find_peaks(current_ss, distance=peak_distance, prominence=peak_prominence), \
                             find_peaks(-current_ss, distance=peak_distance, prominence=peak_prominence)

    # find_peaks returns (indices, dict) but above was wrong unpack; re-run properly:
    peaks_rel, _ = find_peaks(current_ss, distance=peak_distance, prominence=peak_prominence)
    troughs_rel, _ = find_peaks(-current_ss, distance=peak_distance, prominence=peak_prominence)

    # convert to global indices
    peaks = peaks_rel + start_idx
    troughs = troughs_rel + start_idx

    # 4) compute per-cycle ptp using anchors
    # use the steady-state arrays for computing segments but map indices back if needed
    if prefer_anchors == 'peaks' and len(peaks_rel) >= 2:
        ptp_cycles, bounds_rel = compute_cycle_ptps_from_peaks_troughs(current_smooth[start_idx:], peaks_rel, troughs_rel, prefer='peaks')
    elif prefer_anchors == 'troughs' and len(troughs_rel) >= 2:
        ptp_cycles, bounds_rel = compute_cycle_ptps_from_peaks_troughs(current_smooth[start_idx:], peaks_rel, troughs_rel, prefer='troughs')
    else:
        # fallback: if not enough anchors, attempt to build cycles alternating peaks/troughs
        # combine and sort anchors
        anchors_rel = np.sort(np.concatenate([peaks_rel, troughs_rel])) if (len(peaks_rel)>0 or len(troughs_rel)>0) else np.array([])
        ptp_cycles = []
        bounds_rel = []
        for i in range(len(anchors_rel)-1):
            s = anchors_rel[i]
            e = anchors_rel[i+1]
            seg = current_smooth[start_idx + s : start_idx + e + 1]
            if seg.size > 2:
                ptp_cycles.append(seg.max() - seg.min())
                bounds_rel.append((s, e))
        ptp_cycles = np.array(ptp_cycles)

    # map bounds_rel to global indices
    bounds_global = [(start_idx + s, start_idx + e) for (s, e) in bounds_rel]

    result = {
        'ptp_mean': float(np.nan) if ptp_cycles.size == 0 else float(np.nanmean(ptp_cycles)),
        'ptp_std' : float(np.nan) if ptp_cycles.size == 0 else float(np.nanstd(ptp_cycles)),
        'ptp_cycles': ptp_cycles,
        'n_cycles': len(ptp_cycles),
        'start_idx': int(start_idx),
        'peaks': peaks,
        'troughs': troughs,
        'bounds': bounds_global,
        'time_ss': time_ss,
        'current_smooth': current_smooth
    }

    if debug_plot:
        fig, ax = plt.subplots(2,1, figsize=(10,6), sharex=False)
        ax[0].plot(time, current_raw, alpha=0.4, label='raw')
        ax[0].plot(time, current_smooth, label='smoothed')
        ax[0].axvline(time[start_idx], color='k', linestyle='--', label='steady start')
        ax[0].plot(time[peaks], current_smooth[peaks], 'o', label='peaks')
        ax[0].plot(time[troughs], current_smooth[troughs], 'x', label='troughs')
        ax[0].legend()
        ax[0].set_title('Signal and detected anchors')

        # show cycles used
        for (s,e) in bounds_global:
            ax[1].plot(time[s:e+1], current_smooth[s:e+1])
        ax[1].set_title(f'Cycles used (n={len(bounds_global)}), mean P2P={result["ptp_mean"]:.4g}')
        plt.tight_layout()
        plt.show()

    return result

def process_all_datasets(datasets,
                         intensity_levels=None,
                         **process_kwargs):
    """
    datasets: list of dataframes [df1...dfN]
    intensity_levels: list/array of same length with intensity values (if None uses indices 1..N)
    process_kwargs forwarded to process_single_dataset
    Returns dataframe with results and plots the final curve.
    """
    if intensity_levels is None:
        intensity_levels = np.arange(1, len(datasets)+1)

    results = []
    for i, df in enumerate(datasets):
        res = process_single_dataset(df, **process_kwargs)
        res_row = {
            'intensity': intensity_levels[i],
            'ptp_mean': res['ptp_mean'],
            'ptp_std': res['ptp_std'],
            'n_cycles': res['n_cycles'],
            'start_idx': res['start_idx'],
            'troughs' : res['troughs'],
            'details': res
        }
        results.append(res_row)

    results_df = pd.DataFrame(results).sort_values('intensity')

    # Plot peak-to-peak vs intensity


    return results_df

def responsivity_array(iph, power, diameter_cm):
    """
    iph: 1D array (A) photocurrent (IPH = ION - IOFF) per intensity
    power: 1D array (W/cm^2) incident power density per intensity (same length as iph) OR scalar
    diameter_cm: scalar detector diameter in cm
    returns: 1D array of responsivity (A/W)
    """
    iph = np.asarray(iph, dtype=float)
    power = np.asarray(power, dtype=float)
    area = np.pi * (diameter_cm / 2.0)**2   # cm^2
    # if power is given as total power (W) instead of W/cm^2, adapt accordingly.
    R = iph / (area * power)
    return R

def detectivity_array(R, diameter_cm, ioff, tiny_ioff_threshold=1e-30):
    """
    R: 1D array responsivity (A/W) (same length as ioff or scalar)
    diameter_cm: scalar detector diameter (cm)
    ioff: 1D array (A) dark current per intensity OR scalar
    tiny_ioff_threshold: threshold below which we consider Ioff too small (avoid div0)
    returns: 1D array of specific detectivity D* (units: Jones = cm·Hz^0.5/W)
    formula used: D* = R * sqrt(A / (2 * e * |Ioff|))
    """
    R = np.asarray(R, dtype=float)
    ioff = np.asarray(ioff, dtype=float)
    area = np.pi * (diameter_cm / 2.0)**2   # cm^2

    # If ioff is scalar, broadcast it
    if ioff.shape == ():
        ioff = np.full_like(R, float(ioff))

    # Avoid division by zero / extremely small Ioff: mark those entries as NaN
    ioff_abs = np.abs(ioff)
    bad_mask = ioff_abs <= tiny_ioff_threshold
    safe_ioff = ioff_abs.copy()
    safe_ioff[bad_mask] = np.nan  # will produce NaN in detectivity where Ioff is tiny

    Dstar = R * np.sqrt(area / (2.0 * e * safe_ioff))
    return Dstar
