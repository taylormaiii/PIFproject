
const caughtmons = [];

const fusionBox = document.querySelector(".mons-in-box");
const clearButton = document.querySelector(".clear-box");
// add another function that runs the same way that will put the sprite next to the encounter dropdown in the same row
// then figure out how to add the option for an encounter to be fused pokemon, maybe a button that adds a second encounter dropdown
function renderFusionBox() {
    fusionBox.replaceChildren();

    caughtmons.forEach((name) => {
        const card = document.createElement("div");
        card.className = "caught-mon";
        const nameLabel = document.createElement("span");
        nameLabel.textContent = name;

        const cardImage = document.createElement("img");
        const option = Array.from(document.querySelectorAll("option"))
            .find((entry) => entry.value === name);

        if (option?.dataset.pokemonId) {
            cardImage.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${option.dataset.pokemonId}.png`;
            cardImage.alt = `${name} sprite`;
        }

        card.append(cardImage, nameLabel);
        fusionBox.append(card);
    });
}

document.addEventListener("change", (event) => {
    if (!event.target.matches(".status-select")) {
        return;
    }

    const row = event.target.closest("tr");
    const nameInput = row.querySelector(".pokemon-input");
    const name = nameInput.value.trim();

    if (event.target.value === "caught" && name) {
        caughtmons.push(name);
        renderFusionBox();
    }
});

clearButton.addEventListener("click", () => {
    caughtmons.legnth = 0;
    renderFusionBox();
});