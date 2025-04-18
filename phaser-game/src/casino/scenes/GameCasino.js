import { Player } from '../../gameObjects/Player.js';
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
        this.add.image(400, 300, 'sky');

        // this.platforms = this.physics.add.staticGroup();

        // this.platforms.create(400, 568, 'platform').setScale(2).refreshBody();

        // this.platforms.create(600, 400, 'platform');
        // this.platforms.create(50, 250, 'platform');
        // this.platforms.create(720, 220, 'platform');

        this.player = new Player(this, 100, 450);

        this.slots = [];

        let i = 0;
        let x = 150;
        while (i < 12) {
            let newSlots = new SlotMachineDown(this, x, 50).setScale(2.5, 2.5);
            this.slots.push(newSlots);
            i += 1;
            x += 50;
        }

        this.keyW = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
        this.keyA = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
        this.keyS = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
        this.keyD = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);

        // this.stars = this.physics.add.group({
        //     key: 'coin',
        //     repeat: 11,
        //     setXY: {x: 12, y: 0, stepX: 70},
        //     gravityY: 500,
        //     setScale: {x: 2, y:2}
        // });

        // this.physics.add.overlap(this.player, this.stars, this.collectStar, null, this);
        this.physics.add.collider(this.player, this.slots); // adds collision between the player and all slot machines
        for (let i in this.slots) {
            let machine = this.slots[i];
            // machine.refreshBody();
        }

        this.coinCounter = new CoinCounter(this, 28, 28);

        this.websocket = io();  
        this.websocket.on('connect', function() {
            this.emit('connected');
        });
        this.websocket.on('connect_echo', function() {
            console.log('connected to server')
        });
        this.websocket.on('movement', function(data) {
            let recieved_data = data.data
            // console.log('id: ' + recieved_data.id + ', x: ' + recieved_data.x + ', y: ' + recieved_data.y);
        });
        this.timePassed = 0;
        this.timeToNext = 500;
        this.prevPosition = {x: this.player.x, y: this.player.y}
    }

    update(time, delta) {
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
        this.timePassed += delta;
        if (this.timePassed >= this.timeToNext && (this.prevPosition.x != this.player.x || this.prevPosition.y != this.player.y) ) {
            this.prevPosition.x = this.player.x;
            this.prevPosition.y = this.player.y;
            this.websocket.emit('player_move', {'data': {
                'id': 'admin', 
                'x': this.player.x, 
                'y': this.player.y
                }});
        }
    }

    // collectStar(player, star) {
    //     star.disableBody(true, true);
        
    //     this.player.score += 1;
    //     this.scoreText.setText('Stars Collected: ' + this.player.score);
    // }

}