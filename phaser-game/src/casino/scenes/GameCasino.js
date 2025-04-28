import { Player } from '../../gameObjects/Player.js';
import { PlayerGhost } from '../../gameObjects/PlayerGhost.js';
import { CoinCounter } from '../../gameObjects/CoinCounter.js';
import { SlotMachineSide } from '../../gameObjects/SlotMachineSide.js';
import { SlotMachineDown } from '../../gameObjects/SlotMachineDown.js';
import  '../../../../public/socket.io.js';

export class Game extends Phaser.Scene {
    constructor() {
        super('Game');

    }

    create() {
        this.add.image(400, 300, 'sky'); // background image
        this.chScreen = this.add.image(400, 300, 'challenge_screen').setDepth(1);
        this.chTopText = this.add.text(400, 280, '[Player] has challenged you!', { fontSize: '20px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5).setDepth(2);
        this.chBottomText = this.add.text(400, 320, 'E: Accept  SPACE: Deny', { fontSize: '18px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5).setDepth(2);
        this.chScreenVisible(false);

        // id for websockets
        this.socketId;
        // username, assigned value through fetch to phaser/@me
        this.username;

        // array of objects to call update() on
        this.objsToUpdate = [];

        // player object
        this.player = new Player(this, 100, 450);

        // time passed for movement broadcasting
        this.timePassed = 0;
        // how much time needs to pass before broadcasting next movement
        this.timeToNext = 50;
        // previously broadcasted position
        this.prevPosition = {x: this.player.x, y: this.player.x}; 

        this.slots = []; // array for slot machine objects
        this.playerGhosts = {}; // dict for player ghost objects, maps their id to their object

        this.coinCounter = new CoinCounter(this, 28, 28); // coin counter object
        
        // sset of objects player is colliding with
        this.slotOverlaps = new Set();
        this.challengeOverlaps = new Set();

        // populates slots array with 12 slot machines facing down
        let i = 0;
        let x = 150;
        while (i < 12) {
            let newSlots = new SlotMachineDown(this, x, 50);
            this.slots.push(newSlots);
            i += 1;
            x += 50;
        }
        // populates slots array with 12 slot machines facing left and right
        i = 0;
        let y = 200;
        while (i < 6) {
            let newSlots = new SlotMachineSide(this, 374, y, false);
            this.slots.push(newSlots);
            newSlots = new SlotMachineSide(this, 425, y, true);
            this.slots.push(newSlots);
            i += 1;
            y += 50;
        }

        this.playPopup = this.add.image(400, 540, 'popup').setScale(2);
        this.playPopup.text = this.add.text(400, 540, 'Press SPACE to play!', { fontSize: '32px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5);
        this.playPopupVisible(false);

        this.challengePopup = this.add.image(400, 60, 'popup').setScale(2);
        this.challengePopup.text = this.add.text(400, 60, 'Press E to challenge [player]!', { fontSize: '24px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5);
        this.chPopupVisible(false);

        // getting user info
        let request = new Request('/phaser/@me');
        fetch(request).then(response => {
            return response.json();
        }).then(data => {
            this.coinCounter.setCoins(data['coins']);
            this.username = data['username'];
            // broadcasting join message
            this.websocket.emit('casino_join', { 'username': this.username, 'pos': {'x': this.player.x, 'y': this.player.y} });
        });

        // the player that challenged this user, null if none
        this.challenger = null;
        // disables movement & interaction inputs
        this.disableMovement = false;
        // movement keys
        this.keyW = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
        this.keyA = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
        this.keyS = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
        this.keyD = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);
        // interaction keys
        this.keySpace = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
        this.keyE = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.E);

        // websocket initialization
        this.websocket = io();
        this.websocket.scene = this;
        // when recieving message of type "connect_echo"
        this.websocket.on('connect_echo', function(data) {
            this.scene.socketId = data.id;
            console.log('connected to server, my name is ' + this.scene.socketId);
        });
        // when recieving message of type "movement"
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
        // when recieving notice that a player has left the casino
        this.websocket.on('casino_leave', function(data) {
            let username = data['username'];
            this.scene.playerGhosts[username].leave();
            delete this.scene.playerGhosts[username];
        })
        // when recieving a player's coin number
        this.websocket.on('coins', function(data) {
            let username = data['username'];
            if (username != this.scene.username && this.scene.playerGhosts[username] != undefined) {
                this.scene.playerGhosts[username].coinsText.setText('Coins: ' + data['coins']);
            }
        });
        // when recieving a challenge from another user
        this.websocket.on('challenge', function(data) {
            this.scene.disableMovement = true;
            this.scene.challenger = data['from'];
            this.scene.chScreenVisible(true);
        })
        // when a user you challenge accepts
        this.websocket.on('ch_accept', function(data) {
            this.scene.coinflipSwap();
        })
        // when a user you challenge declines
        this.websocket.on('ch_decline', function(data) {
            // TODO
        })
    }

    update(time, delta) {
        // handles player movement
        let moved = false
        if (this.keyA.isDown && !this.disableMovement) {
            this.player.moveLeft();
            moved = true;
        }
        else if (this.keyD.isDown && !this.disableMovement) {
            this.player.moveRight();
            moved = true;
        }
        else {
            this.player.idleX();
        }
        if (this.keyW.isDown && !this.disableMovement) {
            this.player.moveUp();
            moved = true;
        }
        else if (this.keyS.isDown && !this.disableMovement) {
            this.player.moveDown();
            moved = true;
        }
        else {
            this.player.idleY();
        }
        if (!moved) {
            this.player.idle();
        }
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
        if (this.slotOverlaps.size == 0) {
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

    coinflipSwap() {
        this.scene.start('CoinFlip');
        this.websocket.emit('casino_leave', {'username': this.username});
        this.websocket.disconnect(false);
    }

    slotsSwap() {
        this.scene.start('Slots');
        this.websocket.emit('casino_leave', {'username': this.username});
        this.websocket.disconnect(false);
    }
}