// escala de Saaty
const saatyScale = {
    "1/9": "extremely less important",
    "1/8": "extremely less important",
    "1/7": "very strongly less important",
    "1/6": "very strongly less important",
    "1/5": "strongly less important",
    "1/4": "strongly less important",
    "1/3": "moderately less important",
    "1/2": "moderately less important",
    "1": "equally important",
    "2": "moderately more important",
    "3": "moderately more important",
    "4": "strongly more important",
    "5": "strongly more important",
    "6": "very strongly more important",
    "7": "very strongly more important",
    "8": "extremely more important",
    "9": "extremely more important",
};

// manter esse array, porque se aceder os valores pelo dict,
// eles perdem a ordem
const allowedValues = [
    "1/9", "1/8", "1/7", "1/6", "1/5", "1/4", "1/3", "1/2",
    "1", "2", "3", "4", "5", "6", "7", "8", "9"
];

// usada para inverter os valores da escala de Saaty.
// exemplo: "9"->"1/9", "1/9"->"9", etc
function invertValue(input) {
    const index = allowedValues.indexOf(input);
    if (index === -1) {
        throw new Error("Invalid input value");
    } else if (input === "1") {
        return "1";
    }

    // se o valor for valido e diferente de 1, ele inverte,
    // consoante aos allowedValues
    const invertedIndex = allowedValues.length - 1 - index;
    return allowedValues[invertedIndex];
}

// listeners para cada inputs do tipo range
document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function () {
        const valueDisplayAfter = this.nextElementSibling;
        const valueDisplayBefore = this.previousElementSibling;

        // acede os atributos model_i, model_j, e criteria direto dos
        // do div, nos atributos tipo data-model dele
        const model_i = this.closest('.slider-container').dataset.modelI;
        const model_j = this.closest('.slider-container').dataset.modelJ;
        const criteria = this.closest('.slider-container').dataset.criteria;

        // converte para string para poder usar os valores fracionados
        const sliderValue = allowedValues[this.value].toString();

        // não é preciso esse tratamento de "invalid value" mas vou deixar no codigo
        const mappedValue = saatyScale[sliderValue] || "Invalid value";

        if (valueDisplayAfter && valueDisplayAfter.classList.contains('slider-value')) {
            valueDisplayAfter.textContent = sliderValue;
            valueDisplayBefore.textContent = `${model_i.replace(/_/g, ' ')}'s ${criteria.replace(/_/g, ' ')} ${mappedValue} ${model_j.replace(/_/g, ' ')}'s ${criteria.replace(/_/g, ' ')}`;
            // valueDisplayBefore.textContent = `${model_i}'s ${criteria} ${mappedValue} ${model_j}'s ${criteria}`;
        }
    });
});

document.querySelectorAll('input[type="range"]').forEach(slider => {
    // propriedades dos sliders
    slider.min = 0;
    slider.max = allowedValues.length - 1;
    slider.step = 1;
    slider.value = Math.floor((slider.max - slider.min) / 2);

    // atualiza o valor mostrado a direita,
    // usando os valores mapeados
    slider.addEventListener('input', function () {
        const valueDisplay = this.nextElementSibling;
        const mappedValue = allowedValues[this.value];
        if (valueDisplay && valueDisplay.classList.contains('slider-value')) {
            valueDisplay.textContent = mappedValue;
        }
    });

    // inicializa com valor default mapeado
    const valueDisplay = slider.nextElementSibling;
    if (valueDisplay && valueDisplay.classList.contains('slider-value')) {
        valueDisplay.textContent = allowedValues[slider.value];
    }
});

// atualiza inputs das matrizes com valor dos sliders
document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function () {
        const sliderValue = this.value;
        const mappedValue = allowedValues[sliderValue];
        const inverseMappedValue = invertValue(mappedValue);

        // faz a string com os ids dos inputs criterio_i_j e criterio_j_i
        const criteria = this.name.split('-')[1]; // comeca em zero pq a primeira palavra no name eh "range-..."
        const i = this.name.split('-')[2];
        const j = this.name.split('-')[3];
        const textInputId_ij = `text-${criteria}-matrix-${i}-${j}`;
        const textInputId_ji = `text-${criteria}-matrix-${j}-${i}`;

        // busca o input com o id criterio_i_j e altera o valor
        var textInput = document.getElementById(textInputId_ij);
        if (textInput) {
            textInput.value = mappedValue;
        }
        // busca o input com o id criterio_j_i e altera o valor para o inverso
        textInput = document.getElementById(textInputId_ji);
        if (textInput) {
            textInput.value = inverseMappedValue;
        }
    });
});