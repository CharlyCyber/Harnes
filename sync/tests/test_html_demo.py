"""Regression checks for the internal demo module and public router wiring."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


class HtmlDemoTests(unittest.TestCase):
    def test_internal_only_and_routes(self):
        config = json.loads((ROOT / 'sync/targets.json').read_text(encoding='utf-8'))
        self.assertIn('html-demo', config['internal_skills'])
        self.assertNotIn('html-demo', config['profiles']['core'])
        web = (ROOT / 'skills/web/SKILL.md').read_text(encoding='utf-8')
        video = (ROOT / 'skills/video/SKILL.md').read_text(encoding='utf-8')
        demo = (ROOT / 'skills/html-demo/SKILL.md').read_text(encoding='utf-8')
        website = (ROOT / 'skills/video/references/website-demo.md').read_text(encoding='utf-8')
        self.assertIn('html-demo/SKILL.md', web)
        self.assertIn('video/references/website-demo.md', video)
        self.assertIn('simulación', demo)
        self.assertIn('web real', video)
        self.assertIn('--clock real', website)
        self.assertIn('window.__timelines', website)
        for name in ['LICENSE-upstream', 'scripts/StepWindow.jsx', 'scripts/step-window.js',
                     'scripts/step-window.css', 'scripts/shoot.mjs',
                     'references/contract.md', 'references/film.md']:
            self.assertTrue((ROOT / 'skills/html-demo' / name).is_file(), name)

    @unittest.skipUnless(shutil.which('node'), 'Node no disponible')
    def test_vanilla_helpers_and_seekable_clock(self):
        script = ROOT / 'skills/html-demo/scripts/step-window.js'
        code = r'''
const assert = require('node:assert/strict');
require(process.argv[1]);
assert.equal(HTMLDemo.typed('demo', 0.5, 0, 1), 'de');
assert.equal(HTMLDemo.ease(0.5, 0, 1), 0.5);
assert.equal(HTMLDemo.cue(2, [[1, 'a'], [2, 'b']], ''), 'b');
assert.deepEqual(HTMLDemo.glide(1, [[0,0,0,0],[0,2,100,50]], [1]), {x:50,y:25,press:true});
const style = () => ({setProperty() {}});
const cls = () => ({add(){}, toggle(){}});
const view = {clientWidth: 600, style: style(), replaceChildren() {}};
const buttons = [0,1].map(i => ({dataset:{i}, classList:cls(), setAttribute(){}, removeAttribute(){}, addEventListener(){}, querySelector(){return {style:style()}}}));
const el = {classList:cls(), querySelector(){return view}, querySelectorAll(){return buttons}, replaceChildren(){}};
global.document = {hidden:false, createElement(){return {classList:cls(),style:style(),setAttribute(){},append(){},querySelector(){return {}}}}};
global.IntersectionObserver = class {observe(){} disconnect(){}};
global.ResizeObserver = class {observe(){} disconnect(){}};
const steps = [{id:'a',name:'A',dur:2,html:'A'}, {id:'b',name:'B',dur:3,html:'B'}];
const clock = HTMLDemo.mount(el, {steps});
clock.pause(); clock.seek(2.5);
assert.equal(clock.state().i, 1); assert.equal(clock.state().t, 0.5); assert.equal(clock.state().paused, true);
clock.seek(0.25); assert.equal(clock.state().i, 0); assert.equal(clock.state().t, 0.25);
clock.setStill(true); assert.equal(clock.state().t, 2);
clock.play(1); assert.equal(clock.state().t, 3);
clock.destroy();
'''
        result = subprocess.run(['node', '-e', code, str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
