import { SlotMachine } from './SlotMachine.js'

export class SlotMachineSide extends SlotMachine {

    constructor(scene, x, y, flipped) {
        super(scene, x, y, 'slotmachine_side');
        x = -20;
        y = 5;
        if (flipped) {
            this.sprite.flipX = true;
            x = -x;
        }
        this.addOverlapBox(x, y, 2);
    }
}