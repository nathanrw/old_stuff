<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class PeterConsole
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        If disposing AndAlso components IsNot Nothing Then
            components.Dispose()
        End If
        MyBase.Dispose(disposing)
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(PeterConsole))
        Me.Panel1 = New System.Windows.Forms.Panel
        Me.LBL_CurrentPrice = New System.Windows.Forms.Label
        Me.LBL_PetrolPumped = New System.Windows.Forms.Label
        Me.LBL_PumpStatus = New System.Windows.Forms.Label
        Me.Panel2 = New System.Windows.Forms.Panel
        Me.TXT_EnterPricePerLitre = New System.Windows.Forms.TextBox
        Me.BTN_ZeroPumpDisplay = New System.Windows.Forms.Button
        Me.BTN_AlterPricePerLitre = New System.Windows.Forms.Button
        Me.Panel3 = New System.Windows.Forms.Panel
        Me.BTN_ResetDayTotal = New System.Windows.Forms.Button
        Me.LBL_TotalTakings = New System.Windows.Forms.Label
        Me.LBL_TotalPetrolPumped = New System.Windows.Forms.Label
        Me.Panel4 = New System.Windows.Forms.Panel
        Me.LBL_Instructions = New System.Windows.Forms.Label
        Me.Panel5 = New System.Windows.Forms.Panel
        Me.LBL_PTR_INSTR = New System.Windows.Forms.Label
        Me.TMR_Console = New System.Windows.Forms.Timer(Me.components)
        Me.Panel1.SuspendLayout()
        Me.Panel2.SuspendLayout()
        Me.Panel3.SuspendLayout()
        Me.Panel4.SuspendLayout()
        Me.Panel5.SuspendLayout()
        Me.SuspendLayout()
        '
        'Panel1
        '
        Me.Panel1.BackColor = System.Drawing.Color.SteelBlue
        Me.Panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.Panel1.Controls.Add(Me.LBL_CurrentPrice)
        Me.Panel1.Controls.Add(Me.LBL_PetrolPumped)
        Me.Panel1.Controls.Add(Me.LBL_PumpStatus)
        Me.Panel1.Location = New System.Drawing.Point(12, 12)
        Me.Panel1.Name = "Panel1"
        Me.Panel1.Size = New System.Drawing.Size(627, 50)
        Me.Panel1.TabIndex = 2
        '
        'LBL_CurrentPrice
        '
        Me.LBL_CurrentPrice.AutoSize = True
        Me.LBL_CurrentPrice.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_CurrentPrice.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_CurrentPrice.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_CurrentPrice.Location = New System.Drawing.Point(419, 7)
        Me.LBL_CurrentPrice.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_CurrentPrice.Name = "LBL_CurrentPrice"
        Me.LBL_CurrentPrice.Size = New System.Drawing.Size(200, 33)
        Me.LBL_CurrentPrice.TabIndex = 9
        Me.LBL_CurrentPrice.Text = "Current Price: "
        Me.LBL_CurrentPrice.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_PetrolPumped
        '
        Me.LBL_PetrolPumped.AutoSize = True
        Me.LBL_PetrolPumped.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PetrolPumped.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PetrolPumped.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PetrolPumped.Location = New System.Drawing.Point(213, 7)
        Me.LBL_PetrolPumped.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_PetrolPumped.Name = "LBL_PetrolPumped"
        Me.LBL_PetrolPumped.Size = New System.Drawing.Size(200, 33)
        Me.LBL_PetrolPumped.TabIndex = 10
        Me.LBL_PetrolPumped.Text = "Petrol Pumped:"
        Me.LBL_PetrolPumped.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_PumpStatus
        '
        Me.LBL_PumpStatus.AutoSize = True
        Me.LBL_PumpStatus.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PumpStatus.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PumpStatus.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PumpStatus.Location = New System.Drawing.Point(7, 7)
        Me.LBL_PumpStatus.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_PumpStatus.Name = "LBL_PumpStatus"
        Me.LBL_PumpStatus.Size = New System.Drawing.Size(200, 33)
        Me.LBL_PumpStatus.TabIndex = 9
        Me.LBL_PumpStatus.Text = "Pump Status:"
        Me.LBL_PumpStatus.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'Panel2
        '
        Me.Panel2.BackColor = System.Drawing.Color.SteelBlue
        Me.Panel2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.Panel2.Controls.Add(Me.TXT_EnterPricePerLitre)
        Me.Panel2.Controls.Add(Me.BTN_ZeroPumpDisplay)
        Me.Panel2.Controls.Add(Me.BTN_AlterPricePerLitre)
        Me.Panel2.Location = New System.Drawing.Point(12, 68)
        Me.Panel2.Name = "Panel2"
        Me.Panel2.Size = New System.Drawing.Size(381, 90)
        Me.Panel2.TabIndex = 3
        '
        'TXT_EnterPricePerLitre
        '
        Me.TXT_EnterPricePerLitre.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.TXT_EnterPricePerLitre.Location = New System.Drawing.Point(7, 9)
        Me.TXT_EnterPricePerLitre.MinimumSize = New System.Drawing.Size(4, 33)
        Me.TXT_EnterPricePerLitre.Multiline = True
        Me.TXT_EnterPricePerLitre.Name = "TXT_EnterPricePerLitre"
        Me.TXT_EnterPricePerLitre.Size = New System.Drawing.Size(200, 33)
        Me.TXT_EnterPricePerLitre.TabIndex = 0
        Me.TXT_EnterPricePerLitre.Text = "Insert New Price Per Litre"
        Me.TXT_EnterPricePerLitre.TextAlign = System.Windows.Forms.HorizontalAlignment.Center
        '
        'BTN_ZeroPumpDisplay
        '
        Me.BTN_ZeroPumpDisplay.BackColor = System.Drawing.Color.Black
        Me.BTN_ZeroPumpDisplay.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_ZeroPumpDisplay.ForeColor = System.Drawing.SystemColors.ButtonHighlight
        Me.BTN_ZeroPumpDisplay.Location = New System.Drawing.Point(7, 48)
        Me.BTN_ZeroPumpDisplay.Name = "BTN_ZeroPumpDisplay"
        Me.BTN_ZeroPumpDisplay.Size = New System.Drawing.Size(368, 33)
        Me.BTN_ZeroPumpDisplay.TabIndex = 12
        Me.BTN_ZeroPumpDisplay.Text = "Zero Pump Display"
        Me.BTN_ZeroPumpDisplay.UseVisualStyleBackColor = False
        '
        'BTN_AlterPricePerLitre
        '
        Me.BTN_AlterPricePerLitre.BackColor = System.Drawing.Color.Black
        Me.BTN_AlterPricePerLitre.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_AlterPricePerLitre.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.BTN_AlterPricePerLitre.Location = New System.Drawing.Point(213, 9)
        Me.BTN_AlterPricePerLitre.Name = "BTN_AlterPricePerLitre"
        Me.BTN_AlterPricePerLitre.Size = New System.Drawing.Size(162, 33)
        Me.BTN_AlterPricePerLitre.TabIndex = 11
        Me.BTN_AlterPricePerLitre.Text = "Alter Price Per Litre"
        Me.BTN_AlterPricePerLitre.UseVisualStyleBackColor = False
        '
        'Panel3
        '
        Me.Panel3.BackColor = System.Drawing.Color.SteelBlue
        Me.Panel3.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.Panel3.Controls.Add(Me.BTN_ResetDayTotal)
        Me.Panel3.Controls.Add(Me.LBL_TotalTakings)
        Me.Panel3.Controls.Add(Me.LBL_TotalPetrolPumped)
        Me.Panel3.Location = New System.Drawing.Point(399, 68)
        Me.Panel3.Name = "Panel3"
        Me.Panel3.Size = New System.Drawing.Size(240, 125)
        Me.Panel3.TabIndex = 4
        '
        'BTN_ResetDayTotal
        '
        Me.BTN_ResetDayTotal.BackColor = System.Drawing.Color.Black
        Me.BTN_ResetDayTotal.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_ResetDayTotal.ForeColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.BTN_ResetDayTotal.Location = New System.Drawing.Point(7, 84)
        Me.BTN_ResetDayTotal.Name = "BTN_ResetDayTotal"
        Me.BTN_ResetDayTotal.Size = New System.Drawing.Size(225, 33)
        Me.BTN_ResetDayTotal.TabIndex = 11
        Me.BTN_ResetDayTotal.Text = "Reset Day Total"
        Me.BTN_ResetDayTotal.UseVisualStyleBackColor = False
        '
        'LBL_TotalTakings
        '
        Me.LBL_TotalTakings.AutoSize = True
        Me.LBL_TotalTakings.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_TotalTakings.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_TotalTakings.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_TotalTakings.Location = New System.Drawing.Point(7, 6)
        Me.LBL_TotalTakings.MinimumSize = New System.Drawing.Size(225, 33)
        Me.LBL_TotalTakings.Name = "LBL_TotalTakings"
        Me.LBL_TotalTakings.Size = New System.Drawing.Size(225, 33)
        Me.LBL_TotalTakings.TabIndex = 11
        Me.LBL_TotalTakings.Text = "Total Takings: "
        Me.LBL_TotalTakings.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_TotalPetrolPumped
        '
        Me.LBL_TotalPetrolPumped.AutoSize = True
        Me.LBL_TotalPetrolPumped.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_TotalPetrolPumped.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_TotalPetrolPumped.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_TotalPetrolPumped.Location = New System.Drawing.Point(7, 45)
        Me.LBL_TotalPetrolPumped.MinimumSize = New System.Drawing.Size(225, 33)
        Me.LBL_TotalPetrolPumped.Name = "LBL_TotalPetrolPumped"
        Me.LBL_TotalPetrolPumped.Size = New System.Drawing.Size(225, 33)
        Me.LBL_TotalPetrolPumped.TabIndex = 10
        Me.LBL_TotalPetrolPumped.Text = "Total Petrol Pumped: "
        Me.LBL_TotalPetrolPumped.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'Panel4
        '
        Me.Panel4.BackColor = System.Drawing.Color.SteelBlue
        Me.Panel4.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.Panel4.Controls.Add(Me.LBL_Instructions)
        Me.Panel4.Location = New System.Drawing.Point(12, 164)
        Me.Panel4.Name = "Panel4"
        Me.Panel4.Size = New System.Drawing.Size(381, 29)
        Me.Panel4.TabIndex = 5
        '
        'LBL_Instructions
        '
        Me.LBL_Instructions.AutoSize = True
        Me.LBL_Instructions.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_Instructions.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.LBL_Instructions.Location = New System.Drawing.Point(4, 5)
        Me.LBL_Instructions.Name = "LBL_Instructions"
        Me.LBL_Instructions.Size = New System.Drawing.Size(158, 16)
        Me.LBL_Instructions.TabIndex = 0
        Me.LBL_Instructions.Text = "Instructions For Peter:"
        '
        'Panel5
        '
        Me.Panel5.BackColor = System.Drawing.Color.SteelBlue
        Me.Panel5.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.Panel5.Controls.Add(Me.LBL_PTR_INSTR)
        Me.Panel5.Location = New System.Drawing.Point(12, 199)
        Me.Panel5.Name = "Panel5"
        Me.Panel5.Size = New System.Drawing.Size(626, 136)
        Me.Panel5.TabIndex = 6
        '
        'LBL_PTR_INSTR
        '
        Me.LBL_PTR_INSTR.AutoSize = True
        Me.LBL_PTR_INSTR.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PTR_INSTR.ForeColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PTR_INSTR.Location = New System.Drawing.Point(0, 8)
        Me.LBL_PTR_INSTR.Name = "LBL_PTR_INSTR"
        Me.LBL_PTR_INSTR.Size = New System.Drawing.Size(629, 128)
        Me.LBL_PTR_INSTR.TabIndex = 0
        Me.LBL_PTR_INSTR.Text = resources.GetString("LBL_PTR_INSTR.Text")
        '
        'PeterConsole
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.BackColor = System.Drawing.SystemColors.Desktop
        Me.ClientSize = New System.Drawing.Size(650, 347)
        Me.Controls.Add(Me.Panel5)
        Me.Controls.Add(Me.Panel4)
        Me.Controls.Add(Me.Panel3)
        Me.Controls.Add(Me.Panel2)
        Me.Controls.Add(Me.Panel1)
        Me.Name = "PeterConsole"
        Me.Text = "Console"
        Me.Panel1.ResumeLayout(False)
        Me.Panel1.PerformLayout()
        Me.Panel2.ResumeLayout(False)
        Me.Panel2.PerformLayout()
        Me.Panel3.ResumeLayout(False)
        Me.Panel3.PerformLayout()
        Me.Panel4.ResumeLayout(False)
        Me.Panel4.PerformLayout()
        Me.Panel5.ResumeLayout(False)
        Me.Panel5.PerformLayout()
        Me.ResumeLayout(False)

    End Sub
    Friend WithEvents LBL_PetrolPumped As System.Windows.Forms.Label
    Friend WithEvents LBL_PumpStatus As System.Windows.Forms.Label
    Friend WithEvents LBL_CurrentPrice As System.Windows.Forms.Label
    Friend WithEvents Panel3 As System.Windows.Forms.Panel
    Friend WithEvents LBL_TotalTakings As System.Windows.Forms.Label
    Friend WithEvents LBL_TotalPetrolPumped As System.Windows.Forms.Label
    Friend WithEvents BTN_ResetDayTotal As System.Windows.Forms.Button
    Friend WithEvents BTN_ZeroPumpDisplay As System.Windows.Forms.Button
    Friend WithEvents BTN_AlterPricePerLitre As System.Windows.Forms.Button
    Friend WithEvents Panel4 As System.Windows.Forms.Panel
    Friend WithEvents Panel5 As System.Windows.Forms.Panel
    Friend WithEvents TXT_EnterPricePerLitre As System.Windows.Forms.TextBox
    Friend WithEvents LBL_Instructions As System.Windows.Forms.Label
    Friend WithEvents Panel1 As System.Windows.Forms.Panel
    Friend WithEvents Panel2 As System.Windows.Forms.Panel
    Friend WithEvents TMR_Console As System.Windows.Forms.Timer
    Friend WithEvents LBL_PTR_INSTR As System.Windows.Forms.Label
End Class
