export class SlotMachine {

    constructor(scene, x, y, key) {
        this.scene = scene;
        this.sprite = this.scene.physics.add.staticSprite(x, y, key).setScale(2.5, 2.5).refreshBody();

        this.scene.physics.add.collider(this.sprite, this.scene.player);

        this.DEBUG = true;
    }

    addOverlapBox(xOff, yOff, scale) {
        this.overlap = this.scene.physics.add.sprite(this.sprite.x + xOff, this.sprite.y + yOff, 'debug').setScale(scale);
        if (this.DEBUG) {
            this.overlap.setAlpha(0.5);
        } else {
            this.overlap.setAlpha(0);
        }
        this.scene.physics.add.overlap(this.overlap, this.scene.player, this.playerCollide, null, this);
        // this.overlap.refreshBody();
        this.firstOverlap = true;
        this.stoppedOverlap = true;
        this.interacted = false;
    }

    playerCollide() {
        this.stoppedOverlap = false
        if (this.firstOverlap) {
            // console.log('started overlapping')
            this.scene.colliding.add(this);
            this.scene.popupVisible(true);
            this.firstOverlap = false;
        }
        if (this.scene.keySpace.isDown && !this.interacted) {
            // console.log('interacted');
            this.interacted = true;
            this.scene.scene.start('Slots');
        }
        else if (!this.scene.keySpace.isDown && this.interacted) {
            this.interacted = false;
        }
    }

    update() {
        let touching = !this.overlap.body.touching.none || this.overlap.body.embedded;
        let wasTouching = !this.overlap.body.wasTouching.none;
        if (!touching && wasTouching && !this.stoppedOverlap) {
            // console.log('stopped overlapping');
            this.stoppedOverlap = true;
            this.firstOverlap = true;
            this.scene.colliding.delete(this);
            this.scene.stoppedColliding();
        }
    }
}