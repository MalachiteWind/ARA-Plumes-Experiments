from typing import cast
from typing import List

import mitosis
import numpy as np
from ara_plumes.typing import PlumePoints

from pathlib import Path

from plumex.config import data_lookup
from plumex.video_digest import _load_video
from .post_utils import _visualize_fits
from .post_utils import create_edge_func
from .post_utils import plot_raw_frames



trials_folder = Path(__file__).absolute().parents[2] / "trials"

# ignore 862 and 864
# (center_regress_hash, video_lookup_word, edge_regress_hash)
trial_lookup_key = {
    "862": {
        "default": ("85c44b", "low-862", "a52e31")
    },
    "865": {
        "default": ("aedee1", "low-865","264935" )
    }
}


def _unpack_data(
        center_regress_hash:str,
        video_lookup_keyword: str,
        edge_regress_hash: str,
) -> dict:
    
    video, orig_center_fc = _load_video(data_lookup["filename"][video_lookup_keyword])
    center_mitosis_step = mitosis.load_trial_data(
        hexstr=center_regress_hash,
        trials_folder=trials_folder / "center-regress"
    )
    edge_mitosis_step = mitosis.load_trial_data(
        hexstr=edge_regress_hash,
        trials_folder=trials_folder / "edge-regress"
    )

    center_fit_method = center_mitosis_step[1]["main"]
    center_coeff_dc = center_mitosis_step[1]["regressions"][center_fit_method]["data"]

    edge_plume_points = edge_mitosis_step[0]["data"]

    center = cast(List[tuple[int, PlumePoints]], edge_plume_points["center"])
    bot = cast(List[tuple[int, PlumePoints]], edge_plume_points["bottom"])
    top = cast(List[tuple[int, PlumePoints]], edge_plume_points["top"]) 

    top_edge_method, bot_edge_method = edge_mitosis_step[1]["main"]

    edge_coefs_top = np.nanmean(
        edge_mitosis_step[1]["accs"]["top"][top_edge_method]["coeffs"], axis=0
    )
    edge_coefs_bot = np.nanmean(
        edge_mitosis_step[1]["accs"]["bot"][bot_edge_method]["coeffs"], axis=0
    )

    top_func = create_edge_func(edge_coefs_top, top_edge_method)
    bot_func = create_edge_func(edge_coefs_bot, bot_edge_method)

    start_frame = center[0][0]
    end_frame = center[-1][0]

    results = {
        "video": video[start_frame: end_frame+1],
        "center_coef": center_coeff_dc,
        "center_func_method": center_fit_method,
        "center_plume_points": center,
        "top_plume_points": top,
        "bottom_plume_points": bot,
        "top_edge_func": top_func,
        "bot_edge_func": bot_func,
        "start_frame": start_frame,
        "orig_center_fc": orig_center_fc,
    }
    return results



# plot on true points
# _visualize_fits(n_frames=9, **_unpack_data(*trial_lookup_key["865"]["default"]))

# # plot on regression
# _visualize_fits(n_frames=9, **_unpack_data(*trial_lookup_key["865"]["default"]),plot_on_raw_points=False)


video, orig_center_fc = _load_video(data_lookup["filename"]["low-869"])
print(len(video))
plot_raw_frames(video=video[599:],n_frames=4,n_rows=1,n_cols=4)