import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { ExitSign } from '../../gameObjects/ExitSign.js';
import { BetSelector } from '../../gameObjects/BetSelector.js';

export class Slots extends Phaser.Scene {
    constructor() {
        super('Slots');
    }

    create() {
        this.add.image(400, 300, 'slots_bg').setDisplaySize(800, 600);
        this.coinCounter = new CoinCounter(this, 28, 28);

        this.slotsIcons = new SlotsIcons(this, 403, 226);

        this.spinning = false;

        this.exitSign = new ExitSign(this, 730, 32, 'Game');

        this.betSelector = new BetSelector(this, 285, 540);

        // initialize spin button
        this.button = this.add.sprite(700, 500, 'button').setScale(2);
        this.button.scene = this;
        this.button.setInteractive();
        this.button.on('pointerdown', pointer => {
            if (this.spinning) {return}
            this.hideLines();
            this.youWin.setVisible(false);
            this.spinning = true;
            this.slotsIcons.startSpin();
            let currentBet = this.betSelector.bet;
            this.coinCounter.addCoins(-1 * currentBet);
            let request = new Request('/phaser/playSlots', {
                method: "POST",
                body: JSON.stringify({"bet": currentBet}),
                headers: {"Content-Type": "application/json"}
                });
            fetch(request).then(response => {
                if (response.status == 200) {
                    return response.json();
                } else {
                    // HANDLE ERROR
                    return {'error': true};
                }
            }).then(data => {
                if (!data['error']) {
                    setTimeout(function (scene) {
                        scene.coinCounter.setCoins(data['newCoins']);
                        let slots = data['slots'];
                        scene.slotsIcons.setSlots(slots);
                        scene.spinning = false;
                        scene.showLines(data['winningLines']);
                        if (data['winningLines'].length > 0) {
                            scene.youWin.setVisible(true);
                        }
                    }, 1000, this);
                }
            });
        });

        // getting user info
        let request = new Request('/@me');
        fetch(request).then(response => {
            return response.json();
        }).then(data => {
            this.coinCounter.setCoins(data['coins']);
        });

        // initializing line visuals
        this.lines = {};
        this.lines['top left'] = this.add.image(403, 226, 'line_d').setScale(2.5, 2.5).toggleFlipX();
        this.lines['bot left'] = this.add.image(403, 226, 'line_d').setScale(2.5, 2.5);
        this.lines['top'] = this.add.image(403, 99, 'line_h').setScale(3, 2.5);
        this.lines['mid'] = this.add.image(403, 226, 'line_h').setScale(3, 2.5);
        this.lines['bot'] = this.add.image(403, 353, 'line_h').setScale(3, 2.5);
        this.hideLines();

        // you win
        this.youWin = this.add.image(85, 100, 'youwin').setScale(0.5, 0.5);
        this.youWin.setVisible(false);
    }

    showLines(lines) {
        for (let line of lines) {
            this.lines[line].setVisible(true);
        }
    }

    hideLines() {
        for (let line in this.lines) {
            this.lines[line].setVisible(false);
        }
    }
}

class SlotsIcons {
    // 403, 226
    // 262, 99
    constructor(scene, x, y) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.spriteNames = ['coal', 'stone', 'scrip', 'pick', 'crystal', 'gold', 'obsidian', 'diamond'];
        this.iconsMatrix = [[], [], []];
        y -= 127;
        let x_start = x - 141;
        for (let i_y = 0; i_y < 3; i_y++) {
            x = x_start;
            for (let i_x = 0; i_x < 3; i_x++) {
                let sprite = this.scene.add.sprite(x, y, 'slot_icons').setScale(3);
                sprite.anims.create({
                    key: 'spin',
                    frames: sprite.anims.generateFrameNumbers('slot_icons', {start: 0, end: 7}),
                    frameRate: 10,
                    repeat: -1
                });

                for (let sp = 0; sp < 8; sp++) {
                    sprite.anims.create({
                        key: this.spriteNames[sp],
                        frames: sprite.anims.generateFrameNumbers('slot_icons', {start: sp, end: sp})
                    });
                }
                this.iconsMatrix[i_y].push(sprite);
                x += 141;
            }
            y += 127;
        }
        this.randomIcons();
    }

    startSpin() {
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                this.iconsMatrix[y][x].anims.play({key: 'spin', startFrame: randomInt(8)}, true);
            }
        }
    }

    randomIcons() {
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                let r = randomInt(8);
                this.iconsMatrix[y][x].anims.play(this.spriteNames[r]);
            }
        }
    }

    setSlots(slotsMatrix) {
        for (let y = 0; y < 3; y++) {
            for (let x = 0; x < 3; x++) {
                this.iconsMatrix[y][x].anims.play(this.spriteNames[slotsMatrix[y][x]]);
            }
        }
    }

    changeScene() {}
}

function randomInt(max) {
    return Math.floor(Math.random() * 8);
}