import numpy as np
from manim import *
from acdc import CircuitElements as ce
class OpeningScene(Scene):
    r=1;#RADIUS
    f=1;#Frequency
    circle=Mobject;
    origin = Mobject;

    def create_heading(self):
        self.circle = Circle(radius=self.r, color=BLUE)
        heading_1 = Tex("P H A S", font_size=100).next_to(self.circle, LEFT)
        heading_2 = Tex("R S", font_size=100).next_to(self.circle, RIGHT)
        vg = VGroup(self.circle, heading_1, heading_2).move_to(ORIGIN)
        self.origin = Dot(self.circle.get_center(), radius=0.05, color=RED)

        ax1 = Axes(x_range=[0, 5], x_length=5, y_length=2*self.r, axis_config={
            'include_ticks': False
        }, tips=False)
        ax2 = ax1.copy()
        ax1.rotate(PI/2).next_to(self.circle,UP)
        ax2.rotate(-PI/2).next_to(self.circle,DOWN)

        d_theta = ValueTracker(0)
        opacity = ValueTracker(0)
        sine_wave_1 = always_redraw(
            lambda: FunctionGraph(lambda x: np.sin(x + d_theta.get_value()), x_range=[0, 5 * PI]).set_color(
                GREEN).set_stroke(width=4).rotate(PI / 2).next_to(self.circle, UP))
        sine_wave_1.add_updater(lambda t: t.set_stroke(opacity=opacity.get_value()))
        sine_wave_2 = always_redraw(
            lambda: FunctionGraph(lambda x: np.sin((x + d_theta.get_value()) * 2), x_range=[0, 5 * PI]).set_color(
                YELLOW_E).set_stroke(width=4).rotate(-PI / 2).next_to(self.circle, DOWN))
        sine_wave_2.add_updater(lambda t: t.set_stroke(opacity=opacity.get_value()))

        phasor1 = Line(start=self.circle.get_center(), end=self.circle.get_end(), stroke_color=GREEN,
                       stroke_width=3).add_tip(tip_length=0.15).rotate(PI / 2, about_point=self.circle.get_center())
        phasor1.add_updater(lambda t:t.set_stroke(opacity=opacity.get_value()))
        phasor2 = Line(start=self.circle.get_center(), end=self.circle.get_end(), stroke_color=YELLOW_E,
                       stroke_width=3).add_tip(tip_length=0.15).rotate(-PI / 2, about_point=self.circle.get_center())
        phasor2.add_updater(lambda t:t.set_stroke(opacity=opacity.get_value()))
        phasor1_ref = phasor1.copy()
        phasor2_ref = phasor2.copy()
        phasor1.add_updater(
            lambda t: t.become(phasor1_ref.copy()).rotate(d_theta.get_value(), about_point=self.circle.get_center()).set_opacity(opacity.get_value())
        )
        phasor2.add_updater(
            lambda t: t.become(phasor2_ref).rotate(d_theta.get_value() * 2, about_point=self.circle.get_center()).set_opacity(opacity.get_value())
        )

        self.add(sine_wave_1,sine_wave_2,phasor1,phasor2)
        self.play(DrawBorderThenFill(vg),rate_func=lambda t:t**4)
        self.play(FadeIn(VGroup(ax1,ax2)),opacity.animate.set_value(1),d_theta.animate.set_value(-5),rate_func=linear,run_time=3)
        self.play(d_theta.animate.set_value(-50),rate_func=linear,run_time=30)
        #self.play(FadeOut(VGroup(vg,ax1,ax2)),opacity.animate.set_value(0),d_theta.animate.set_value(-15),rate_func=linear,run_time=3)
        self.wait()

    def construct(self):
        self.create_heading()

class AC_Intro_1(Scene):


    def construct(self):
        #Create Circuit
        cell = ce.get_cell()
        switch_o = ce.get_open_switch()
        switch_c = ce.get_closed_switch()
        bulb = ce.get_bulb()
        ground = ce.get_ground()

        cell.rotate(-PI / 2).move_to(LEFT * 3)
        switch_o.move_to(UP * 2)
        switch_c.move_to(UP * 2)
        bulb.rotate(PI / 2).move_to(RIGHT * 3)
        ground.move_to(DOWN * 2)
        element_grp1 = VGroup(cell, switch_o, bulb, ground)
        circuit1 = ce.connect_series([(cell,UP,switch_o,LEFT),(switch_o,RIGHT,bulb,UP),(bulb,DOWN,ground,UP),(ground,UP,cell,DOWN)])
        circuit_grp = VGroup(element_grp1,circuit1)
        self.play(Create(circuit_grp),run_time = 4 ,rate_functions=linear)
        self.wait(duration = 2)
        self.play(circuit_grp.animate.shift(LEFT*3))
        self.wait()
        #Current and Voltage definition
        #self.add(circuit_grp.shift(LEFT*3))
        voltage_sub_text1 = Tex("Electric Potential")
        voltage_sub_text2 = Tex("V").set_color(GREEN)
        voltage_sub_text3 = Tex("volts (V)")
        voltage_text= VGroup(voltage_sub_text1,voltage_sub_text2,voltage_sub_text3).arrange(DOWN).shift(RIGHT*3)
        self.play(ShowIncreasingSubsets(voltage_text),run_time = 4,rate_func=linear)
        self.wait()
        self.play(FadeOut(voltage_sub_text1,voltage_sub_text3),
                  voltage_sub_text2.animate.next_to(cell,RIGHT))
        #self.add(voltage_text)
        #self.remove(voltage_sub_text1,voltage_sub_text3)
        #self.play(voltage_sub_text2.animate.next_to(cell,RIGHT))
        #self.add(voltage_sub_text2)

        current_sub_text1 = Tex("Electric Current")
        current_sub_text2 = Tex("I").set_color(BLUE)
        current_sub_text3 = Tex("amperes (A)")
        current_text = VGroup(current_sub_text1,current_sub_text2,current_sub_text3).arrange(DOWN).shift(RIGHT*3)
        #self.add(current_text)
        self.play(ShowIncreasingSubsets(current_text),run_time=4, rate_func= linear)
        self.wait()
        #self.play(current_sub_text2.animate.next_to(switch_o,UL,buff=0))
        self.play(FadeOut(current_sub_text1,current_sub_text3),
                  current_sub_text2.animate.next_to(switch_o,UL,buff=0))
        self.wait()
        #self.add(current_sub_text2)

        hill_vertices = [
            np.array([0,3,0]),
            np.array([3,3,0]),
            np.array([3,0,0]),
            np.array([5,0,0]),
        ]
        hill = CubicBezier(*hill_vertices).shift(DR)
        ball = Circle(radius=0.25,fill_color=RED,fill_opacity=1)
        ball.move_to(hill.point_from_proportion(0)).shift(UP/4)
        #self.add(hill,ball)
        self.play(Create(VGroup(hill,ball)))
        self.wait()
        height_measure = DoubleArrow(start=np.array(([hill.get_start()[0],hill.get_end()[1],0])),end=hill.get_start(),tip_length=0.25,stroke_width=1,buff=0.1)
        h = Tex('height').scale(0.75)
        h.next_to(height_measure,RIGHT)
        #self.add(height_measure,h)
        self.play(GrowArrow(height_measure),Write(h))
        self.play(Indicate(h),Indicate(voltage_sub_text2))
        self.wait()

        ball_direction = Arrow(start=hill.get_start(),end=hill.get_end(),tip_length=0.25,stroke_width=1).scale(0.25).shift(UP*1.5)
        current_direction = Arrow(start=LEFT,end=RIGHT,tip_length=0.25,stroke_width=1).next_to(current_sub_text2,RIGHT)
        #self.add(ball_direction)
        #self.wait()

        charge1 = Dot(color=RED).move_to(circuit1.get_start())
        #self.add(charge1)
        switch_c.move_to(switch_o.get_center())
        self.play(Indicate(current_sub_text2))
        self.play(FadeOut(switch_o),FadeIn(switch_c),GrowArrow(ball_direction),GrowArrow(current_direction))
        self.play(MoveAlongPath(ball,hill.copy().set_opacity(0).shift(UP/4)),MoveAlongPath(charge1,ce.get_closed_path(circuit1,False)),run_time=4)
        self.play(FadeOut(VGroup(charge1,ball,hill,ball_direction,current_direction,height_measure,h,switch_c)),FadeIn(switch_o))
        self.wait()
        self.play(VGroup(circuit_grp,voltage_sub_text2,current_sub_text2).animate.shift(RIGHT*3))
        self.wait()

class AC_Intro_2(Scene):
    def construct(self):
        cell = ce.get_cell()
        switch_o = ce.get_open_switch()
        switch_c = ce.get_closed_switch()
        bulb = ce.get_bulb()
        ground = ce.get_ground()

        cell.rotate(-PI / 2).move_to(LEFT * 3)
        switch_o.move_to(UP * 2)
        switch_c.move_to(UP * 2)
        bulb.rotate(PI / 2).move_to(RIGHT * 3)
        ground.move_to(DOWN * 2)
        element_grp1 = VGroup(cell, switch_o, bulb, ground)
        circuit1 = ce.connect_series([(cell, UP, switch_o, LEFT), (switch_o, RIGHT, bulb, UP), (bulb, DOWN, ground, UP),
                                      (ground, UP, cell, DOWN)])
        circuit_grp = VGroup(element_grp1, circuit1)

        V = Tex("V").set_color(GREEN)
        I = Tex("I").set_color(BLUE)
        positive = VGroup(Tex("+",font_size=50).set_color(RED), Circle(color=RED,radius=0.25,stroke_width=1.5)).scale(0.65)
        negative = VGroup(Tex("-",font_size=100).set_color(DARK_BLUE), Circle(color=DARK_BLUE,radius=0.25,stroke_width=1.5)).scale(0.65)
        V.next_to(cell,RIGHT)
        I.next_to(switch_o,UL,buff=0)
        current_direction = Arrow(start=LEFT,end=RIGHT,tip_length=0.25,stroke_width=1).next_to(I,RIGHT)
        positive.next_to(cell,UL,buff=-0.2)
        negative.next_to(cell,DL,buff=-0.2)

        #self.add(NumberPlane().add_coordinates())
        self.add(circuit_grp,V,I)
        self.play(Create(positive))
        self.wait()
        self.play(Indicate(positive))
        self.play(Create(negative))
        self.wait(duration=2)

        self.play(FadeOut(switch_o),FadeIn(switch_c),GrowArrow(current_direction))
        self.wait()

        rev = ValueTracker(0)
        charges = VGroup(*[Dot(color=RED) for _ in range(20)])
        def dot_pos(mob):
            delay = 0
            v = rev.get_value()
            for smob in mob.submobjects:
                r = delay+v
                while np.greater_equal(r,1):
                    r -= 1
                smob.move_to(ce.get_closed_path(circuit1,False).point_from_proportion(r))
                delay+=0.05
            return mob
        self.add(charges)
        charges.add_updater(dot_pos)

        self.play(rev.animate.set_value(2),rate_func=linear,run_time = 15)
        rev.set_value(0)
        self.play(positive.animate.scale(1.5),negative.animate.scale(1.5),rev.animate.set_value(2),rate_func=linear,run_time = 7)
        rev.set_value(0)
        self.play(positive.animate.scale(0.25), negative.animate.scale(.25), rev.animate.set_value(1),rate_func=linear, run_time=7)
        self.wait()

class AC_Intro_3(Scene):
    def construct(self):
        cell = ce.get_cell()
        switch_o = ce.get_open_switch()
        switch_c = ce.get_closed_switch()
        bulb = ce.get_bulb()
        ground = ce.get_ground()

        cell.rotate(-PI / 2).move_to(LEFT * 3)
        switch_o.move_to(UP * 2)
        switch_c.move_to(UP * 2)
        bulb.rotate(PI / 2).move_to(RIGHT * 3)
        ground.move_to(DOWN * 2)
        element_grp1 = VGroup(cell, switch_o, bulb, ground)
        circuit1 = ce.connect_series([(cell, UP, switch_o, LEFT), (switch_o, RIGHT, bulb, UP), (bulb, DOWN, ground, UP),
                                      (ground, UP, cell, DOWN)])
        circuit_grp = VGroup(element_grp1, circuit1)

        V = Tex("V").set_color(GREEN)
        I = Tex("I").set_color(BLUE)
        positive = VGroup(Tex("+", font_size=50).set_color(RED),
                          Circle(color=RED, radius=0.25, stroke_width=1.5)).scale(0.65)
        negative = VGroup(Tex("-", font_size=100).set_color(DARK_BLUE),
                          Circle(color=DARK_BLUE, radius=0.25, stroke_width=1.5)).scale(0.65)
        V.next_to(cell, RIGHT)
        I.next_to(switch_o, UL, buff=0)
        current_direction = Arrow(start=RIGHT, end=LEFT, tip_length=0.25, stroke_width=1).next_to(I, LEFT)
        positive.next_to(cell, DL, buff=-0.2)
        negative.next_to(cell, UL, buff=-0.2)

        # self.add(NumberPlane().add_coordinates())
        self.add(circuit_grp, V, I)
        self.play(Rotate(
            cell,axis=[0,0,1],angle=PI
        ))
        self.wait(duration = 5)
        self.play(Create(positive))
        self.wait()
        self.play(Create(negative))
        self.wait()
        self.play(FadeOut(switch_o),FadeIn(switch_c),GrowArrow(current_direction))
        self.wait()

        rev = ValueTracker(1)
        charges = VGroup(*[Dot(color=RED) for _ in range(20)])
        def dot_pos(mob):
            delay = 0
            v = rev.get_value()
            for smob in mob.submobjects:
                r = delay + v
                while np.greater_equal(r, 1):
                    r -= 1
                smob.move_to(ce.get_closed_path(circuit1, False).point_from_proportion(r))
                delay += 0.05
            return mob
        self.add(charges)
        charges.add_updater(dot_pos)
        self.play(rev.animate.set_value(0), rate_func=linear, run_time=15)
        self.wait()








