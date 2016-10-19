Public Class FRM_Pump

    Public TicksPerSecond As Integer = 1
    Public Ticks As Integer
    Public LitresPerSecond As Single = 1
    Public PetrolPumped As Single = 0
    Public PricePerLitre As Single = PeterConsole.PricePerLitre
    Public CurrentPrice As Single = 0

    Sub ChangeColours(ByVal Col1, ByVal Col2, ByVal Col3, ByVal Col4, ByVal status)
        BTN_Remove.BackColor = Col1
        BTN_Start.BackColor = Col2
        BTN_Stop.BackColor = Col3
        BTN_Replace.BackColor = Col4
        PeterConsole.PumpStatus = status
        LBL_PMP_Status.Text = PeterConsole.PumpStatus
    End Sub

    Public Sub SetPPL(ByVal ppl)
        PricePerLitre = ppl
        LBL_PPL_VAL.Text = "£" & PricePerLitre
    End Sub

    Public Sub RefreshCounters()
        LBL_TPHO_VAL.Text = Ticks
        LBL_PP_VAL.Text = PetrolPumped
        LBL_CC_VAL.Text = CurrentPrice
    End Sub

    Private Sub Pump_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        ChangeColours(Color.Black, Color.Gray, Color.Gray, Color.Gray, "Replaced")
        LBL_PPL_VAL.Text = "£" & PricePerLitre
    End Sub

    Private Sub BTN_Remove_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_Remove.Click
        If PeterConsole.PumpStatus = "Replaced" Then
            ChangeColours(Color.Gray, Color.Black, Color.Gray, Color.Black, "Removed")
        End If
    End Sub

    Private Sub BTN_Start_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_Start.Click
        If PeterConsole.PumpStatus = "Removed" Then
            ChangeColours(Color.Gray, Color.Gray, Color.Black, Color.Gray, "Started")
        End If
    End Sub

    Private Sub BTN_Stop_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_Stop.Click
        If PeterConsole.PumpStatus = "Started" Then
            ChangeColours(Color.Gray, Color.Black, Color.Gray, Color.Black, "Removed")
        End If
    End Sub

    Private Sub BTN_Replace_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_Replace.Click
        If PeterConsole.PumpStatus = "Removed" Then
            ChangeColours(Color.Black, Color.Gray, Color.Gray, Color.Gray, "Replaced")
        End If
    End Sub

    Private Sub TMR_Petrol_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles TMR_Petrol.Tick
        If PeterConsole.PumpStatus = "Started" Then
            Ticks = Ticks + 1
            LBL_TPHO_VAL.Text = Ticks & " s"
            PetrolPumped += LitresPerSecond
            LBL_PP_VAL.Text() = Math.Round(PetrolPumped, 2) & " l"
            CurrentPrice += LitresPerSecond * PricePerLitre
            LBL_CC_VAL.Text = "£" & Math.Round(CurrentPrice, 2)
            PeterConsole.Show_Info_Top(PeterConsole.PumpStatus, PetrolPumped, CurrentPrice)
        End If
    End Sub

End Class