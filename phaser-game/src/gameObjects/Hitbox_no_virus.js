export class Hitbox extends Phaser.Physics.Arcade.Sprite {
    
    constructor(scene, parent, x, y, scale) {
        super(scene, x, y, 'debug');
        // parent needs functions: startOverlap(), duringOverlap(), and stopOverlap().
        this.parent = parent;
        this.setScale(scale);
        this.scene.add.existing(this);
        this.scene.physics.add.existing(this);
        // adds self to update list so it can recieve updates from scene
        this.scene.objsToUpdate.push(this);

        // controls visibility of all hitboxes
        this.DEBUG = true;

        if (this.DEBUG) {
            this.setAlpha(0.5);
        } else {
            this.setAlpha(0);
        }

        this.firstOverlap = true;
        this.stoppedOverlap = true;
        this.wasEmbedded = false;
    }

    addOverlap(object) {
        this.scene.physics.add.overlap(this, object, this.onOverlap, null, this);
    }

    onOverlap() {
        this.stoppedOverlap = false
        if (this.firstOverlap) {
            // console.log('started overlapping')
            this.firstOverlap = false;
            this.parent.startOverlap();
            
        }
        this.parent.duringOverlap();
    }

    update() {
        let touching = !this.body.touching.none || this.body.embedded;
        let wasTouching = !this.body.wasTouching.none || this.wasEmbedded;
        if (!touching && wasTouching && !this.stoppedOverlap) {
            // console.log('stopped overlapping');
            this.stoppedOverlap = true;
            this.firstOverlap = true;
            this.parent.stopOverlap();
        }
        this.wasEmbedded = this.body.embedded;
    }
}