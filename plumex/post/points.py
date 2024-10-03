from pathlib import Path
from typing import Any
from typing import Optional

from ara_plumes import PLUME
from mitosis import _load_trial_params
from mitosis import load_trial_data

from plumex.video_digest import _load_video

trials = {"good": "e64149"}
trials_folder = Path(__file__).absolute().parents[2] / "trials"
points_trials_folder = trials_folder / "center"

trial_info = {
    trial_tag: (
        load_trial_data(hexstr, trials_folder=points_trials_folder),
        _load_trial_params(hexstr, step=0, trials_folder=points_trials_folder),
    )
    for trial_tag, hexstr in trials.items()
}


def mini_video_digest(
    filename: str,
    frame: int,
    fixed_range: tuple[int, int] = (0, -1),
    gauss_space_kws: Optional[dict[str, Any]] = None,
    gauss_time_kws: Optional[dict[str, Any]] = None,
    circle_kw: Optional[dict[str, Any]] = None,
    contour_kws: Optional[dict[str, Any]] = None,
):
    raw_vid, orig_center = _load_video(filename)
    clean_vid = PLUME.clean_video(
        raw_vid,
        fixed_range,
        gauss_space_blur=True,
        gauss_time_blur=True,
        gauss_space_kws=gauss_space_kws,
        gauss_time_kws=gauss_time_kws,
    )
    img_range = (frame, frame + 1)
    center, bottom, top = PLUME.video_to_ROM(
        clean_vid,
        orig_center,
        img_range,
        concentric_circle_kws=circle_kw,
        get_contour_kws=contour_kws,
    )


frame = 500
