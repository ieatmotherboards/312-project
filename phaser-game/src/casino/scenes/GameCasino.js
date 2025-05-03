import { Player } from '../../gameObjects/Player.js';
import { PlayerGhost } from '../../gameObjects/PlayerGhost.js';
import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { SlotMachineSide } from '../../gameObjects/SlotMachineSide.js';
import { SlotMachineDown } from '../../gameObjects/SlotMachineDown.js';
import { MineEntrance } from '../../gameObjects/MineEntrance.js';
import { RouletteTable } from '../../gameObjects/RouletteTable.js';
import { ExitSignHREF } from '../../gameObjects/ExitSignHREF.js'
import  '../../../../public/socket.io.js';

export class Game extends Phaser.Scene {
    constructor() {
        super('Game');

    }

    create() {
    // INITIAL GRAPHICS
        // casino floor repeating texture
        this.add.tileSprite(400, 300, 800, 600, 'back');
        // screen for when another player challenges you to a coin toss
        this.chScreen = this.add.image(400, 300, 'challenge_screen').setDepth(1);
        this.chTopText = this.add.text(400, 280, '[Player] has challenged you!', { fontSize: '20px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5).setDepth(2);
        this.chBottomText = this.add.text(400, 320, 'E: Accept  SPACE: Deny', { fontSize: '18px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5).setDepth(2);
        this.chScreenVisible(false);
        // player's coin counter
        this.coinCounter = new CoinCounter(this, 28, 28);

        new ExitSignHREF(this, 720, 0, '/').setOrigin(.5, 0);

    // INSTANCE VARS
        // this player's username, assigned value through fetch to phaser/@me
        this.username;
        // id for websockets
        this.socketId;
        // array of objects to call update() on
        this.objsToUpdate = [];
        // time passed for movement broadcasting
        this.timePassed = 0;
        // how much time needs to pass before broadcasting next movement
        this.timeToNext = 50;
        // the player that challenged this user, null if none
        this.challenger = null;
        // disables movement & interaction inputs
        this.disableMovement = false;

        // array containing slot machine objects
        this.slots = [];
        // dict for player ghost objects, maps their username to their object
        this.playerGhosts = {};
        // sets of hitboxes player is overlapping
        this.gameOverlaps = new Set();
        this.challengeOverlaps = new Set();
        
        
    // GAME OBJECT INIT
        // player object
        this.player = new Player(this, 100, 450);
        // previously broadcasted position
        this.prevPosition = {x: this.player.x, y: this.player.x}; 

        // populates slots array with 10 slot machines facing down
        let i = 0;
        let x = 150;
        while (i < 10) {
            let newSlots = new SlotMachineDown(this, x, 50);
            this.slots.push(newSlots);
            i += 1;
            x += 50;
        }
        // populates slots array with 10 slot machines facing left and right
        i = 0;
        let y = 200;
        while (i < 5) {
            let newSlots = new SlotMachineSide(this, 374, y, false);
            this.slots.push(newSlots);
            newSlots = new SlotMachineSide(this, 425, y, true);
            this.slots.push(newSlots);
            i += 1;
            y += 50;
        }

        new RouletteTable(this, 185, 530);
        new RouletteTable(this, 400, 530);
        new RouletteTable(this, 615, 530);

        // popup to play games
        this.playPopup = this.add.image(400, 540, 'popup').setScale(2);
        this.playPopup.text = this.add.text(400, 540, 'Press SPACE to play!', { fontSize: '32px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5);
        this.playPopupVisible(false);
        // popup to challenge players
        this.challengePopup = this.add.image(400, 60, 'popup').setScale(2);
        this.challengePopup.text = this.add.text(400, 60, 'Press E to challenge [player]!', { fontSize: '24px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5);
        this.chPopupVisible(false);

        // mines entrance
        this.mineEnter = new MineEntrance(this, 780, 300);

    // GETTING USER INFO
        let request = new Request('/@me');
        fetch(request).then(response => {
            return response.json();
        }).then(data => {
            this.coinCounter.setCoins(data['coins']);
            this.username = data['username'];
            let textureKey = 'user_' + this.username;
            // broadcasting join message
            this.websocket.emit('casino_join', { 'username': this.username, 'pos': {'x': this.player.x, 'y': this.player.y} });
            if (this.textures.exists(textureKey)) {
                this.player.setTexture(textureKey);
            } else {
                this.load.image(textureKey, data['pfp_path']);
                this.load.once(Phaser.Loader.Events.COMPLETE, () => {
                    this.player.setTexture(textureKey);
                    this.player.setDisplaySize(34, 34);
                }, this);
                this.load.start();
            }
        });
        

    // INPUT KEYS
        // movement keys
        this.keyW = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
        this.keyA = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
        this.keyS = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
        this.keyD = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);
        // interaction keys
        this.keySpace = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
        this.keyE = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.E);

    // WEBSOCKETS
        // websocket initialization
        this.websocket = io();
        this.websocket.scene = this;
        // server acknowledges connection
        this.websocket.on('connect_echo', function(data) {
            this.scene.socketId = data.id;
            console.log('connected to server, my name is ' + this.scene.socketId);
        });
        // recieving player movement data
        this.websocket.on('movement', function(data) {
            let x = data['pos']['x'];
            let y = data['pos']['y'];
            let user = data['username'];
            let scene_user = this.scene.username;
            if (scene_user != undefined && user != scene_user) {
                if (!(user in this.scene.playerGhosts)) {
                    let ghost = new PlayerGhost(this.scene, x, y, user);
                    ghost.move(x, y);
                    this.scene.playerGhosts[user] = ghost;
                    this.scene.websocket.emit('get_coins', { 'username': user });
                } else {
                    let ghost = this.scene.playerGhosts[user];
                    ghost.move(x, y);
                }
            }
        });
        // player leaves casino
        this.websocket.on('casino_leave', function(data) {
            let username = data['username'];
            this.scene.playerGhosts[username].leave();
            delete this.scene.playerGhosts[username];
        })
        // recieving player's coin count
        this.websocket.on('coins', function(data) {
            let username = data['username'];
            if (username != this.scene.username && this.scene.playerGhosts[username] != undefined) {
                this.scene.playerGhosts[username].coinsText.setText('Coins: ' + data['coins']);
            }
        });
        // recieving a challenge from another user
        this.websocket.on('challenge', function(data) {
            this.scene.disableMovement = true;
            this.scene.challenger = data['from'];
            this.scene.chScreenVisible(true);
        })
        // a user you challenge accepts
        this.websocket.on('ch_accept', function(data) {
            this.scene.coinflipSwap();
        })
        // a user you challenge declines
        this.websocket.on('ch_decline', function(data) {
            // TODO
        })
    }

    // called every tick
    update(time, delta) {
        // handles player movement
        let x = 0;
        let y = 0;
        if (!this.disableMovement) {
            if (this.keyA.isDown) {
                x -= 200;
            }
            if (this.keyD.isDown) {
                x += 200;
            }
            if (this.keyW.isDown) {
                y -= 200;
            }
            if (this.keyS.isDown) {
                y += 200;
            }
        }
        this.player.move(x, y);
        // handles challenge accept or deny
        if (this.challenger != null) {
            let accepted = null;
            if (this.keySpace.isDown) {
                accepted = false;
            } else if (this.keyE.isDown) {
                accepted = true;
            }
            if (accepted != null) {
                this.websocket.emit('challenge_response', {
                    'accepted': accepted, 
                    'acceptor': this.username, 
                    'challenger': this.challenger
                });
            }
            if (accepted == true) {
                this.coinflipSwap();
            } else if (accepted == false) {
                this.challenger = null;
                this.disableMovement = false;
                this.chScreenVisible(false);
            }
        }
        // handles movement broadcasting
        if (this.timePassed >= this.timeToNext) {
            if (this.username != undefined && (this.prevPosition.x != this.player.x || this.prevPosition.y != this.player.y)) {
                this.timePassed -= this.timeToNext;
                this.prevPosition.x = this.player.x;
                this.prevPosition.y = this.player.y;
                this.websocket.emit('player_move', {
                    'username': this.username, 
                    'pos': {
                        'x': this.player.x, 
                        'y': this.player.y
                    }});
            }
        } else {
            this.timePassed += delta;
        }
        // handles GameObject updates
        for (let x in this.objsToUpdate) {
            this.objsToUpdate[x].update();
        }
    }

    stoppedColliding() {
        if (this.gameOverlaps.size == 0) {
            this.playPopupVisible(false);
        }
        if (this.challengeOverlaps.size == 0) {
            this.chPopupVisible(false);
        }
    }

    playPopupVisible(x) {
        this.playPopup.visible = x;
        this.playPopup.text.visible = x;
    }

    chPopupVisible(x) {
        this.challengePopup.visible = x;
        this.challengePopup.text.visible = x;
    }

    chScreenVisible(x) {
        this.chScreen.visible = x;
        this.chTopText.visible = x;
        this.chBottomText.visible = x;
    }

    chPopupText(text) {
        this.challengePopup.text.setText("Press E to challenge " + text + " !");
    }

    sceneSwap(sceneKey) {
        this.scene.start(sceneKey);
        this.websocket.disconnect(false);
    }

    coinflipSwap() {
        this.sceneSwap('CoinFlip');
    }

    slotsSwap() {
        this.sceneSwap('Slots');
    }

    minesSwap() {
        this.sceneSwap('Mines');
    }

    rouletteSwap() {
        window.location.href = '/roulette';
    }
}