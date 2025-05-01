import { Hitbox } from './Hitbox_no_virus.js';

export class PlayerGhost extends Phaser.GameObjects.GameObject {

    constructor(scene, x, y, username) {
        super(scene, "ghost_" + username);
        this.sprite = this.scene.add.sprite(x, y, 'pfp').setDisplaySize(34, 34);
        this.border = this.scene.add.sprite(x, y, 'ghost').setDisplaySize(34, 34);
        this.username = username;

        this.nameText = this.scene.add.text(this.x, this.y + 30, username, { fontSize: '14px', align: 'center', color: '#000', fontStyle: "bold"}).setOrigin(0.5, 0.5);
        this.coinsText = this.scene.add.text(this.x, this.y - 30, 'Coins: 0', { fontSize: '12px', align: 'center', color: '#000'}).setOrigin(0.5, 0.5);

        this.hitbox = new Hitbox(this.scene, this, this.x, this.y, 4);
        this.hitbox.addOverlap(this.scene.player)

        this.interacted = false;

        // GETTING USER INFO
        let textureKey = 'user_' + this.username;
        if (this.scene.textures.exists(textureKey)) {
            this.sprite.setTexture(textureKey);
        } else {
            let request = new Request('/@user/' + this.username);
            fetch(request).then(response => {
                return response.json();
            }).then(data => {
                this.scene.load.image(textureKey, data['pfp_path']);
                this.scene.load.once(Phaser.Loader.Events.COMPLETE, () => {
                    this.sprite.setTexture(textureKey);
                    this.sprite.setDisplaySize(34, 34);
                }, this);
                this.scene.load.start();
            });
        }
    }

    move(x, y) {
        this.sprite.setX(x).setY(y);
        this.border.setX(x).setY(y);
        this.hitbox.setX(x).setY(y);
        this.nameText.setX(x).setY(y + 30);
        this.coinsText.setX(x).setY(y - 30);
    }

    startOverlap() {
        this.scene.slotOverlaps.add(this);
        this.scene.chPopupVisible(true);
    }

    duringOverlap() {
        if (this.scene.keyE.isDown && !this.interacted) {
            this.interacted = true;
            // when interacting:
            this.scene.websocket.emit('challenge_player', {
                'challenger': this.scene.username,
                'defender': this.username
            });
        }
        else if (!this.scene.keyE.isDown && this.interacted) {
            this.interacted = false;
        }
    }

    stopOverlap() {
        this.scene.challengeOverlaps.delete(this);
        this.scene.stoppedColliding();
    }

    leave() {
        let hb_idx = this.scene.objsToUpdate.indexOf(this.hitbox);
        this.scene.objsToUpdate.splice(hb_idx, 1)
        this.hitbox.destroy();
        this.sprite.destroy();
        this.nameText.destroy();
        this.coinsText.destroy();
        this.destroy();
    }
}