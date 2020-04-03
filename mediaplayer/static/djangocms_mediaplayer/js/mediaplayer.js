let loadPlayer = (container) => {
    const mediaElement = container.getElementsByClassName("media-element")[0];
    mediaElement.controls = false;

    let skip_time = 15; // in seconds
    const videoPlayBtn = container.getElementsByClassName('video-wrapper')[0];
    const playPauseBtn = container.getElementsByClassName('play-btn')[0];
    const stopBtn = container.getElementsByClassName('stop-btn')[0];
    const rewindBtn = container.getElementsByClassName('rewind-btn')[0];
    const fastForwardBtn = container.getElementsByClassName('fast-forward-btn')[0];
    const progressSlider = container.getElementsByClassName('slider')[0];
    const progress = container.getElementsByClassName('progress')[0];
    const progressBar = container.getElementsByClassName('progress-bar')[0];
    const playtimeDuration = container.getElementsByClassName('playtime-duration')[0];
    const playtimeCurrent = container.getElementsByClassName('playtime-current')[0];
    const muteBtn = container.getElementsByClassName('mute-btn')[0];
    const volumeInput = container.getElementsByClassName('volume-slider')[0];
    const fullscreen = container.getElementsByClassName('fullscreen-btn')[0];

    if (videoPlayBtn) {
        videoPlayBtn.addEventListener('click', () => {
            mediaElement.paused ?  mediaElement.play() : mediaElement.pause();
            iconPlaying.classList.toggle('playing')
        });
    }

    // buttons
    const iconPlaying = playPauseBtn.getElementsByClassName('icon-state')[0];
    const iconVolume = container.getElementsByClassName('icon-volume')[0];

    playPauseBtn.addEventListener('click', (e) => {
        mediaElement.paused ?  mediaElement.play() : mediaElement.pause();
        iconPlaying.classList.toggle('playing')
    });

    stopBtn.addEventListener('click', () => {
        mediaElement.currentTime = 0;
        mediaElement.pause();
    });

    if (fastForwardBtn && rewindBtn) {
        fastForwardBtn.addEventListener('click', () => {
            if (mediaElement.currentTime + skip_time < mediaElement.duration ) {
                mediaElement.currentTime += skip_time;
            } else {
                mediaElement.pause();
                mediaElement.currentTime = mediaElement.duration;
            }
        });
        rewindBtn.addEventListener('click', () => {
            if (mediaElement.currentTime - skip_time > 0) {
                mediaElement.currentTime -= skip_time;
            } else {
                mediaElement.currentTime = 0;
            }
        });
    }

    muteBtn.addEventListener('click', () => {
        mediaElement.muted = !mediaElement.muted;
        if (!mediaElement.muted) {
            volumeInput.value = logToPosition(mediaElement.volume * 100);
        } else {
            volumeInput.value = 0;
        }
        iconVolume.classList.toggle('mute')
    });

    mediaElement.addEventListener('loadedmetadata', function() {
        // set up video btn
        if (videoPlayBtn) {
            if (mediaElement.paused) {
                videoPlayBtn.classList.remove('playing');
            } else {
                videoPlayBtn.classList.add('playing');
            }
        }

        // set up progress bars
        let _duration = Math.round(mediaElement.duration).toString();
        if (progressBar) {
            progress.value = mediaElement.currentTime;
            progress.setAttribute('max', _duration);
        }
        if (progressSlider) {
            progressSlider.value = mediaElement.currentTime;
            progressSlider.setAttribute('max', _duration);
        }

        playtimeDuration.innerText = parsePlayTime(mediaElement.duration);
        playtimeCurrent.innerText = parsePlayTime(mediaElement.currentTime);

        // change mute icon
        if (mediaElement.muted) {
            volumeInput.value = 0;
            iconVolume.classList.add('mute');
        }
    });

    let mouseMovement = true;
    let mouseMovementTimeout = null;
    mediaElement.addEventListener('timeupdate', function() {
        // update video play button
        if (videoPlayBtn) {
            if (mediaElement.paused) {
                videoPlayBtn.classList.remove('playing');
            } else {
                videoPlayBtn.classList.add('playing');
            }
        }

        if (videoPlayBtn) {// hacky-style: check if is video
            window.onmousemove = function(e) {
                mouseMovement = true;
                if (mouseMovementTimeout) {
                    clearTimeout(mouseMovementTimeout);
                }
                mouseMovementTimeout = setTimeout(function () {
                    mouseMovement = false;
                }, 1300)
            };
        }

        if (!mouseMovement) {
            container.classList.add('hide-controls');
        } else {
            container.classList.remove('hide-controls');
        }

        // update vol range
        mediaElement.muted ? volumeInput.value = 0 : volumeInput.value = logToPosition(mediaElement.volume * 100);

        if (progressSlider) {
            progressSlider.value = mediaElement.currentTime;
        }

        // set current time
        playtimeCurrent.innerText = parsePlayTime(mediaElement.currentTime);

        if (progressBar) {
            progress.value = mediaElement.currentTime;
            progressBar.style.width = Math.floor((mediaElement.currentTime / mediaElement.duration) * 100) + '%';
        }

        // update buttons
        // playing
        if (!mediaElement.paused) {
            iconPlaying.classList.add('playing');
        } else {
            iconPlaying.classList.remove('playing')
        }
        // mute
        if (mediaElement.muted) {
            iconVolume.classList.add('mute');
        } else {
            iconVolume.classList.remove('mute')
        }


    });

    if (progressSlider) {
        progressSlider.addEventListener('change', () => {
            mediaElement.currentTime = progressSlider.value;
        });
    }

    volumeInput.addEventListener('input', () => {
        mediaElement.muted = false;
        mediaElement.volume = Math.round(logVolume(volumeInput.value)) / 100;
        iconVolume.classList.remove('mute')
    });


    if (fullscreen) {
        let fullScreenEnabled = !!(document.fullscreenEnabled || document.mozFullScreenEnabled || document.msFullscreenEnabled || document.webkitSupportsFullscreen || document.webkitFullscreenEnabled || document.createElement('video').webkitRequestFullScreen);
        if (!fullScreenEnabled) {
            fullscreen.style.display = 'none';
        }

        fullscreen.addEventListener('click', () => {
            handleFullscreen();
        });

        let isFullScreen = function() {
            return !!(document.fullScreen || document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || document.fullscreenElement);
        };

        let setFullscreenData = function(state) {
            container.setAttribute('data-fullscreen', !!state);
        };

        let handleFullscreen = () => {
            if (isFullScreen()) {
                if (document.exitFullscreen) document.exitFullscreen();
                else if (document.mozCancelFullScreen) document.mozCancelFullScreen();
                else if (document.webkitCancelFullScreen) document.webkitCancelFullScreen();
                else if (document.msExitFullscreen) document.msExitFullscreen();
                setFullscreenData(false);
            }
            else {
                if (container.requestFullscreen) container.requestFullscreen();
                else if (container.mozRequestFullScreen) container.mozRequestFullScreen();
                else if (container.webkitRequestFullScreen) container.webkitRequestFullScreen();
                else if (container.msRequestFullscreen) container.msRequestFullscreen();
                setFullscreenData(true);
            }
        };

        document.addEventListener('fullscreenchange', function(e) {
            setFullscreenData(!!(document.fullScreen || document.fullscreenElement));
        });
        document.addEventListener('webkitfullscreenchange', function() {
            setFullscreenData(!!document.webkitIsFullScreen);
        });
        document.addEventListener('mozfullscreenchange', function() {
            setFullscreenData(!!document.mozFullScreen);
        });
        document.addEventListener('msfullscreenchange', function() {
            setFullscreenData(!!document.msFullscreenElement);
        });
    }
};

// calc log volume
let logVolume = (position, min_position=0, max_position=100) => {
    if (position < 1) {
        return 0;
    }
    let minv = Math.log(1);
    let maxv = Math.log(100);
    // calculate adjustment factor
    let scale = (maxv-minv) / (max_position - min_position);

    return Math.exp(minv + scale*(position-min_position));
};

function logToPosition(value, min_position = 0, max_position = 100) {
    let minv = Math.log(1);
    let maxv = Math.log(100);
    // calculate adjustment factor
    let scale = (maxv-minv) / (max_position - min_position);
    return (Math.log(value)-minv) / scale + min_position;
}

let parsePlayTime = (time_in_s) => {
    time_in_s = Math.round(time_in_s);
    let m = Math.floor(time_in_s  / 60);
    let s = time_in_s - m * 60;

    // m = m.toString().padStart(2, '0');
    s = s.toString().padStart(2, '0');

    return `${m}:${s}`;
};

let init = () => {
    let instances = document.getElementsByClassName('mediaplayer-container');
    instances = Array.from(instances);

    instances.map((container) => {
        loadPlayer(container);
    });
};

init();