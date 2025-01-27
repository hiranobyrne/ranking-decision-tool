
// createSliderHandler(1, 'A', 'B');
function createSliderHandler(loop_index, model_i, model_j) {
    const slider = document.getElementById(`discrete-slider-${loop_index}-${model_i}-${model_j}`);
    const sliderValue = document.getElementById(`slider-value-${loop_index}-${model_i}-${model_j}`);

    // atualiza valor
    slider.oninput = function() {
        sliderValue.innerHTML = this.value;
    };
}
