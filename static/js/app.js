
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
    const inputs = row.querySelectorAll(".pokemon-input");
    const names = Array.from(inputs)
        .map(input => input.value.trim())
        .filter(Boolean);


    const previousNames = row.dataset.caughtMons
        ? JSON.parse(row.dataset.caughtMons)
        : [];

    previousNames.forEach(name => {
        const index = caughtmons.indexOf(name);

        if (index !== -1) {
            caughtmons.splice(index, 1);
        }
    });

    if (event.target.value === "caught") {
        names.forEach(name => {
            caughtmons.push(name);
        });
        row.dataset.caughtMons = JSON.stringify(names);
    } else {
        row.dataset.caughtMons = JSON.stringify([]);
    }

    renderFusionBox();
    });

document.addEventListener("change", (event) => {
    if (!event.target.matches(".pokemon-input")) {
        return;
    }

    const input = event.target;
    const row = input.closest("tr");
    const name = input.value.trim();

    renderRowSprites(row, name);
});

clearButton.addEventListener("click", () => {
    caughtmons.length = 0;
    document.querySelectorAll(".h-location-row").forEach(row => {
    row.dataset.caughtMons = JSON.stringify([]);
    });
    renderFusionBox();
});

function onClickAdd(button) {
    const container = button.closest(".encounter-container");
    const inputsContainer = container.querySelector(".encounter-inputs");
    const inputs = inputsContainer.querySelectorAll(".encounter-input");

    if (inputs.length === 1) {
        const clone = inputs[0].cloneNode(true);
        const input = clone.querySelector(".pokemon-input");
        input.value = "";
        inputsContainer.appendChild(clone);
        button.textContent = "Unfuse";
    } else {
        inputs[1].remove();
        button.textContent = "Fuse";
    }
}

function renderRowSprites(row, name) {
    const spritecol = row.querySelector(".spriteimg");
    const spriteimg = document.createElement("div");
    spriteimg.className = "caught-sprite";
    const spriteimgname = document.createElement("span");
    spriteimgname.textContent = name;
    const spriteimgimg = document.createElement("img");
    const option = Array.from(document.querySelectorAll("option"))
            .find((entry) => entry.value === name);
    if (option?.dataset.pokemonId) {
        spriteimgimg.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${option.dataset.pokemonId}.png`;
        spriteimgimg.alt = `${name} sprite`; }

    spriteimg.append(spriteimgimg, spriteimgname);
    spritecol.append(spriteimg);

}