from manim import *
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
        self.play(d_theta.animate.set_value(-20),rate_func=linear,run_time=9)
        #self.play(FadeOut(VGroup(vg,ax1,ax2)),opacity.animate.set_value(0),d_theta.animate.set_value(-15),rate_func=linear,run_time=3)
        self.wait()
