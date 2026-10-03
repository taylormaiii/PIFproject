const caughtmons = [];

const fusionBox = document.querySelector(".mons-in-box");
const clearButton = document.querySelector(".clear-box");
const clearRow = document.querySelector(".clear-row");
let lastClearedBox = null;
const sortOptions = document.querySelector(".sortOptions");
let currentSort = "TOTAL";
let lastFusionResults = [];


if (sortOptions) {
  sortOptions.addEventListener("change", (event) => {
    currentSort = event.target.value;
    if (lastFusionResults.length) {
      renderFusionResults(lastFusionResults);
    }
  })}


const evolutionToggle = document.querySelector("#evolution-toggle");
let includeEvolutions = false;

if (evolutionToggle) {
    evolutionToggle.addEventListener("change", (event) => {
        includeEvolutions = event.target.checked;

        if (caughtmons.length >= 2) {
            submitFusion();
        }
    });
}


function renderFusionBox() {
    fusionBox.replaceChildren();

    caughtmons.forEach((name) => {
        const card = document.createElement("div");
        card.className = "caught-mon";
        const nameLabel = document.createElement("span");
        nameLabel.textContent = name;
        const hide = document.createElement("button");
        hide.id = "hideButton"
        hide.style.backgroundColor = "black"
        hide.onclick = () => onClickHide(hide);
        

        const cardImage = document.createElement("img");
        const option = Array.from(document.querySelectorAll("option"))
            .find((entry) => entry.value === name);

        if (option?.dataset.pokemonId) {
            cardImage.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${option.dataset.pokemonId}.png`;
            cardImage.alt = `${name} sprite`;

        }

        card.append(cardImage, nameLabel, hide);
        fusionBox.append(card);
    });
}

function onClickDel(button) {
    const row = button.closest(".h-location-row");

    if (!row) {
        return;
    }

    const previousNames = row.dataset.caughtMons
        ? JSON.parse(row.dataset.caughtMons)
        : [];

    previousNames.forEach(name => {
        let index = caughtmons.indexOf(name);

        while (index !== -1) {
            caughtmons.splice(index, 1);
            index = caughtmons.indexOf(name);
        }
    });

    row.querySelectorAll(".pokemon-input").forEach(input => {
        input.value = "";
    });

    const inputsContainer = row.querySelector(".encounter-inputs");
    const inputs = inputsContainer.querySelectorAll(".encounter-input");

    if (inputs.length > 1) {
        inputs[1].remove();
    }

    row.querySelector(".fuse-button").textContent = "Fuse";
    row.querySelector(".status-select").value = "Select";
    row.dataset.caughtMons = JSON.stringify([]);

    renderRowSprites(row);
    renderFusionBox();
}

function onClickHide(button) {
    const pokeCard = button.closest(".caught-mon");

    if (!pokeCard) {
        return;
    }

    pokeCard.style.backgroundColor = pokeCard.style.backgroundColor === "grey"
        ? ""
        : "grey";
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
    submitFusion();
    });

document.addEventListener("change", (event) => {
    if (!event.target.matches(".pokemon-input")) {
        return;
    }

    const input = event.target;
    const row = input.closest("tr");
    renderRowSprites(row);
});

function saveBoxState() {
    lastClearedBox = {
    mons: [...caughtmons],
    rows: Array.from(document.querySelectorAll(".h-location-row")).map(row => ({
        row,
        caughtMons: row.dataset.caughtMons
    }))
}}

function clearBox() {
    saveBoxState();
    caughtmons.length = 0;
    document.querySelectorAll(".h-location-row").forEach(row => {
    row.dataset.caughtMons = JSON.stringify([]);
    });
    renderFusionBox();
    document.querySelector(".fused-possible").replaceChildren();
};

clearButton.addEventListener("click", clearBox);

function undoClearBox() {
    if (!lastClearedBox) {
        return;
    }

    caughtmons.length = 0;
    caughtmons.push(...lastClearedBox.mons);

    lastClearedBox.rows.forEach(({ row, caughtMons }) => {
        row.dataset.caughtMons = caughtMons;
    });

    renderFusionBox();
    lastClearedBox = null;
};

const undoButton = document.querySelector(".undo-box");
undoButton.addEventListener("click", undoClearBox);

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

function renderRowSprites(row) {
    const spritecol = row.querySelector(".spriteimg");
    const inputs = Array.from(row.querySelectorAll(".pokemon-input"));
    const names = inputs.map(input => input.value.trim()).filter(Boolean);
    const options = inputs.map(input => Array.from(document.querySelectorAll("option"))
        .find(entry => entry.value === input.value.trim()));
    const ids = options.map(option => option?.dataset.pokemonId);
    const isFusion = inputs.length === 2 && ids.every(Boolean);

    spritecol.replaceChildren();

    if (!names.length) {
        return;
    }

    const spriteimg = document.createElement("div");
    spriteimg.className = "caught-sprite";
    const spriteimgname = document.createElement("span");
    spriteimgname.textContent = names.join(" + ");
    const spriteimgimg = document.createElement("img");
    if (isFusion) {
        spriteimgimg.src = `https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/${ids[0]}.${ids[1]}.png`;
        spriteimgimg.alt = `${names.join(" + ")} fused sprite`;
    } else if (ids[0]) {
        spriteimgimg.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${ids[0]}.png`;
        spriteimgimg.alt = `${names[0]} sprite`;
    }

    spriteimg.append(spriteimgimg, spriteimgname);
    spritecol.append(spriteimg);

}

async function submitFusion() {
    if (caughtmons.length < 2) {
        return;
    }

    const formData = new FormData();

    caughtmons.forEach(name => {
        formData.append("caughtmon", name);
    });

    formData.append("include_evolutions", includeEvolutions);

    const response = await fetch("/", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    renderFusionResults(data.results);
}


// check if sprite has alternates ex. ${result['fusionid']}a.png or b or c etc and if a,b,c etc exist, give a swap sprite variant button and show that sprite instead


function renderFusionResults(results) {
    lastFusionResults = results
    const allCards = results.flatMap(pair => pair.variants)
    allCards.sort((a, b) => {
    const valueA = Number(a.stats?.[currentSort] ?? 0);
    const valueB = Number(b.stats?.[currentSort] ?? 0);
    return valueB - valueA;
  });
    

    document.querySelector(".fused-possible").replaceChildren();
    allCards.forEach(result => {
    const fusedCard = document.createElement("div");
    fusedCard.className = "possible-fusions relative z-0 flex shrink-0 flex-col items-stretch overflow-hidden rounded-lg transition-all duration-200";
    const fusedCardSprite = document.createElement("img")
    fusedCardSprite.addEventListener("error", brokenCard);
    fusedCardSprite.className = "fusion-sprite relative z-10 w-full overflow-visible"
    fusedCardSprite.src = `https://ifd-spaces.sfo2.cdn.digitaloceanspaces.com/custom/${result['fusionid']}.png`;
    const fusedCardName = document.createElement("span");
    fusedCardName.className = "fusion-name relative z-10 w-full flex-col flex px-1 "
    fusedCardName.textContent = `${result.head} + ${result.body}`;
    const types = Array.isArray(result.types) ? result.types : [];
    if (types.length === 1) {
        const fusedCardType = document.createElement("img");
        fusedCardType.src = `https://fusioncalc.com/images/type/card/${types[0]}.png`;
        fusedCardType.className = "fused-type-solo relative z-10 w-full justify-center mt-0.5 gap-1 flex"
        fusedCard.append(fusedCardName, fusedCardSprite, fusedCardType);
    } else if (types.length >= 2) {
        const fusedCardTypes1 = document.createElement("img");
        const fusedCardTypes2 = document.createElement("img");
        const type1 = types[0];
        const type2 = types[1];
        fusedCardTypes1.src = `https://fusioncalc.com/images/type/card/${type1}.png`;
        fusedCardTypes2.src = `https://fusioncalc.com/images/type/card/${type2}.png`;
        fusedCardTypes1.className = "fused-type-duo relative z-10 w-full justify-center mt-0.5 gap-1 flex"
        fusedCardTypes2.className = "fused-type-duo relative z-10 w-full justify-center mt-0.5 gap-1 flex"
        fusedCard.append(fusedCardName, fusedCardSprite, fusedCardTypes1, fusedCardTypes2);
    }
    fusedCard.dataset.head = result.head;
    fusedCard.dataset.body = result.body;
    fusedCard.addEventListener("click", openFusionDetails);

    document.querySelector(".fused-possible").append(fusedCard);
})}

async function openFusionDetails(event) {
  const card = event.currentTarget;
  const modal = document.getElementById("themodal");

  try {
    const response = await fetch("/api/fusion-details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        head: card.dataset.head,
        body: card.dataset.body
      })
    });

    if (!response.ok) {
      throw new Error(`Fusion details request failed: ${response.status}`);
    }

    const details = await response.json();
    const pairDetails = details[0];
    const leftVariant = pairDetails.variants[0];
    const rightVariant = pairDetails.variants[1];

    document.querySelector(".modalnames1").textContent = `${leftVariant.head} + ${leftVariant.body}`;
    document.querySelector(".modalsprite1").innerHTML = `<img src="${leftVariant.sprite}" alt="${leftVariant.head} + ${leftVariant.body}">`;
    document.querySelector(".modaltypes1").innerHTML = renderTypeImages(leftVariant.types);
    document.querySelector(".modalstats1").textContent = JSON.stringify(leftVariant.stats, null, 2);
    document.querySelector(".modalabilities1").textContent = [
      ...(Array.isArray(leftVariant.abilities) ? leftVariant.abilities : []),
      ...(Array.isArray(leftVariant["hidden abilities"]) ? leftVariant["hidden abilities"] : [])
    ].filter(Boolean).join(", ");

    document.querySelector(".modalnames2").textContent = `${rightVariant.head} + ${rightVariant.body}`;
    document.querySelector(".modalsprite2").innerHTML = `<img src="${rightVariant.sprite}" alt="${rightVariant.head} + ${rightVariant.body}">`;
    document.querySelector(".modaltypes2").innerHTML = renderTypeImages(rightVariant.types);
    document.querySelector(".modalstats2").textContent = JSON.stringify(rightVariant.stats, null, 2);
    document.querySelector(".modalabilities2").textContent = [
      ...(Array.isArray(rightVariant.abilities) ? rightVariant.abilities : []),
      ...(Array.isArray(rightVariant["hidden abilities"]) ? rightVariant["hidden abilities"] : [])
    ].filter(Boolean).join(", ");

    modal.classList.add("open");
  } catch (error) {
    console.error("Error loading fusion details:", error);
  }
}

function renderTypeImages(types) {
  return (Array.isArray(types) ? types : []).map(type => {
    return `<img src="https://fusioncalc.com/images/type/card/${type}.png" alt="${type}" />`;
  }).join("");
}

function closeFusionModal() {
  const modal = document.getElementById("themodal");
  if (modal) {
    modal.classList.remove("open");
  }
}

const modalCloseButton = document.querySelector(".modal-close-button");
if (modalCloseButton) {
  modalCloseButton.addEventListener("click", closeFusionModal);
}

const fusionModal = document.getElementById("themodal");
if (fusionModal) {
  fusionModal.addEventListener("click", (event) => {
    if (event.target === fusionModal) {
      closeFusionModal();
    }
  });
}

function brokenCard (event) {
    const failedImageCard = event.currentTarget
    const failedCard = failedImageCard.closest(".possible-fusions")
    failedCard.classList.add("broken");
};


function CustomToggle() {
    const toggle = document.getElementById('toggle-custom')
    const brokenCards = document.querySelectorAll(".possible-fusions.broken");
    
    brokenCards.forEach(card => {
        card.classList.toggle("hideCard",toggle.checked && card.classList.contains("broken")
);
    });
}

document.getElementById("toggle-custom").addEventListener("change", CustomToggle);