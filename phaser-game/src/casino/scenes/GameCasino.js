import { Player } from '../../gameObjects/Player.js';
import { PlayerGhost } from '../../gameObjects/PlayerGhost.js'
import { CoinCounter } from '../../gameObjects/CoinCounter.js'
import { SlotMachineSide } from '../../gameObjects/SlotMachineSide.js'
import { SlotMachineDown } from '../../gameObjects/SlotMachineDown.js'
import  '../../../../public/socket.io.js'

export class Game extends Phaser.Scene {
    constructor() {
        super('Game');

    }

    // this file has lots of commented out code from the tutorial i followed
    create() {
        this.add.image(400, 300, 'sky'); // background image

        this.socketId = ''; // id for websockets

        this.player = new Player(this, 100, 450); // player object

        this.timePassed = 0;    // time passed for movment broadcasting
        this.timeToNext = 50;  // how much time needs to pass before broadcasting next movement
        this.prevPosition = {x: this.player.x, y: this.player.y} // previously broadcasted position

        this.slots = []; // array for slot machine objects
        this.playerGhosts = {}; // dict for player ghost objects, maps their id to their object

        this.coinCounter = new CoinCounter(this, 28, 28); // coin counter object

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

        // movement keys
        this.keyW = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
        this.keyA = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
        this.keyS = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
        this.keyD = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);

        // websocket initialization
        this.websocket = io();
        this.websocket.scene = this;
        //// when connected to server
        // this.websocket.on('connect', function() {
        //     this.emit('connected');
        // });
        // when recieving message of type "connect_echo"
        this.websocket.on('connect_echo', function(data) {
            this.scene.socketId = data.id;
            console.log('connected to server, my name is ' + this.scene.socketId);
        });
        // when recieving message of type "movement"
        this.websocket.on('movement', function(data) {
            let recieved_data = data.data;
            let x = recieved_data.x;
            let y = recieved_data.y;
            let id = recieved_data.id;
            if (id != this.scene.socketId) {
                if (!(id in this.scene.playerGhosts)) {
                    this.scene.playerGhosts[id] = new PlayerGhost(this.scene, x, y);
                } else {
                    let ghost = this.scene.playerGhosts[id];
                    ghost.sprite.setX(x).setY(y);
                }
            }
            // console.log('id: ' + recieved_data.id + ', x: ' + recieved_data.x + ', y: ' + recieved_data.y);
        });
    }

    update(time, delta) {
        // handles player movement
        let moved = false
        if (this.keyA.isDown) {
            this.player.moveLeft();
            moved = true;
        }
        else if (this.keyD.isDown) {
            this.player.moveRight();
            moved = true;
        }
        else {
            this.player.idleX();
        }
        if (this.keyW.isDown) {
            this.player.moveUp();
            moved = true;
        }
        else if (this.keyS.isDown) {
            this.player.moveDown();
            moved = true;
        }
        else {
            this.player.idleY();
        }
        if (!moved) {
            this.player.idle();
        }
        // handles movement broadcasting
        if (this.timePassed >= this.timeToNext) {
            if (this.prevPosition.x != this.player.x || this.prevPosition.y != this.player.y) {
                this.timePassed -= this.timeToNext;
                this.prevPosition.x = this.player.x;
                this.prevPosition.y = this.player.y;
                this.websocket.emit('player_move', {'data': {
                    'id': this.socketId, 
                    'x': this.player.x, 
                    'y': this.player.y
                    }});
            }
        } else {
            this.timePassed += delta;
        }
    }

    // collectStar(player, star) {
    //     star.disableBody(true, true);
        
    //     this.player.score += 1;
    //     this.scoreText.setText('Stars Collected: ' + this.player.score);
    // }

}